from flask import Flask, render_template, request
import os
import test
import pytesseract
import image_to_text
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if not allowed_file(file.filename):
            return "Invalid file type. Only text files are allowed."

        language = request.form.get("language")
        if not language:
            return "No language selected"

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            test.run_test(file.filename, language)
        except ValueError as e:
            return f"Error processing file: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

        return f"""
            File {file.filename} processed and converted to speech in {language}.
            <a href='/run-test'>View Output</a>
        """
    return render_template("index.html")

@app.route("/run-test")
def run_test_route():
    return render_template("output.html")

@app.route("/image_to_text", methods=["GET", "POST"])
def image_to_text():
    return render_template("image_to_text.html")
if __name__ == "__main__":
    app.run(debug=True)
