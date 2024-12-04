from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
from PIL import Image
import pytesseract
import test

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/suveer/Desktop/Tooler/users.db'  # Correct path to SQLite DB
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for sessions
db = SQLAlchemy(app)

# Define paths for uploading and saving files
UPLOAD_FOLDER = '/Users/suveer/Desktop/Tooler/uploads/text_uploads/'
TEXT_OUTPUT_PATH = '/Users/suveer/Desktop/Tooler/uploads/image_content.txt'
AUDIO_OUTPUT_FOLDER = '/Users/suveer/Desktop/Tooler/outputs/audio/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_OUTPUT_FOLDER'] = AUDIO_OUTPUT_FOLDER

# Ensure directories exist
for folder in [UPLOAD_FOLDER, AUDIO_OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# User model with first name, last name, email, and password (no hashing for simplicity)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Home route
@app.route('/')
def home_page():
    return render_template('index.html')

# Sign Up route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('login'))
        except:
            flash('Email already exists!', category='error')
            return redirect(url_for('sign_up'))

    return render_template('sign_up.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login successful!', category='success')
            return redirect(url_for('landing_page'))
        else:
            flash('Login failed. Check your credentials and try again.', category='error')

    return render_template('login.html')

# Landing page route after login
@app.route('/landing_page')
def landing_page():
    if 'user_id' not in session:
        flash('You need to login first.', category='error')
        return redirect(url_for('login'))

    return render_template('landing_page.html')

# Text to Audio page route
@app.route('/text_to_audio', methods=['POST', 'GET'])
def text_to_audio():
    if request.method == 'POST':
        file = request.files.get('file')
        language = request.form.get('language')

        if file and language:
            if file.filename.endswith('.txt'):
                filename = str(uuid.uuid4()) + '.txt'
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Save the uploaded file
                try:
                    file.save(file_path)
                    print(f"File saved at: {file_path}")
                except Exception as e:
                    print(f"Error saving file: {e}")
                    flash("Error saving the file.", category='error')
                    return redirect(url_for('text_to_audio'))

                try:
                    # Read the text from the file
                    with open(file_path, 'r', encoding='utf-8') as text_file:
                        text = text_file.read()
                    
                    if not text.strip():
                        flash("The text file is empty.", category='error')
                        return redirect(url_for('text_to_audio'))

                    # Call the run_test method to convert text to audio
                    audio_output = test.run_test(text, language)

                    if audio_output:
                        audio_path = os.path.join(app.config['AUDIO_OUTPUT_FOLDER'], 'output.mp3')

                        # Save audio data to an mp3 file
                        try:
                            with open(audio_path, 'wb') as audio_file:
                                audio_file.write(audio_output.read())  # Write binary audio data
                                print(f"Audio saved at: {audio_path}")
                        except Exception as e:
                            print(f"Error writing audio file: {e}")
                            flash("Error saving audio file.", category='error')
                            return redirect(url_for('text_to_audio'))

                        # Return the generated audio file for immediate playback
                        return render_template('audio_preview.html', audio_file='output.mp3')

                    else:
                        flash("Audio conversion failed.", category='error')
                except Exception as e:
                    print(f"Error processing the file: {e}")
                    flash(f"Error processing the file: {e}", category='error')
            else:
                flash("Please upload a valid .txt file.", category='error')
        else:
            flash("File or language not provided!", category='error')
            return redirect(url_for('text_to_audio'))

    return render_template('text_to_audio.html')

# Image to Text route
@app.route('/image_to_text', methods=['GET', 'POST'])
def image_to_text():
    result = None
    image_file = None
    text_file = None

    if request.method == 'POST':
        image_file = request.files.get('image_file')

        if image_file:
            if image_file.filename.split('.')[-1].lower() in ['png', 'jpg', 'jpeg']:
                filename = str(uuid.uuid4()) + '.' + image_file.filename.split('.')[-1]
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                try:
                    image_file.save(file_path)
                    image = Image.open(file_path)
                    text = pytesseract.image_to_string(image)

                    if text.strip():
                        text_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image_content.txt')
                        with open(text_filename, 'w') as text_file:
                            text_file.write(text)

                        flash("Text extracted successfully!", category='success')
                        result = text
                        text_file = 'image_content.txt'
                    else:
                        flash("No text extracted from the image.", category='error')
                except Exception as e:
                    flash(f"Error processing the image: {e}", category='error')
            else:
                flash("Invalid file type. Only PNG, JPG, and JPEG are allowed.", category='error')
        else:
            flash("No image file received.", category='error')

    return render_template('image_to_text.html', result=result, image_file=image_file, text_file=text_file)

# Download file route
@app.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the database and tables if they do not exist
    app.run(debug=True)
