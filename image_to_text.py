from PIL import Image
import pytesseract
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_and_save_text(image_file, upload_folder):
    if image_file is None:
        return "No image file provided."

    # Check if the file has a valid extension
    if not allowed_file(image_file.filename):
        return "Invalid file type. Only image files (png, jpg, jpeg) are allowed."

    try:
        # Save the image to the server
        filename = image_file.filename
        file_path = os.path.join(upload_folder, filename)
        image_file.save(file_path)

        # Open the image and verify if it's valid
        try:
            image = Image.open(file_path)
            image.verify()  # Verify it's a valid image
        except (IOError, SyntaxError) as e:
            return f"Invalid image file. Error: {str(e)}"

        # Convert the image to RGB if it is not in an acceptable mode
        if image.mode not in ['RGB', 'L']:
            image = image.convert('RGB')

        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image)

        # If no text is extracted
        if not extracted_text.strip():
            return "No text extracted from the image."

        # Define the output text file path
        text_output_path = os.path.join(upload_folder, 'image_content.txt')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(text_output_path), exist_ok=True)

        # Save the extracted text to the text file
        with open(text_output_path, 'w') as output_file:
            output_file.write(extracted_text)

        # Return a success message with download links for both the image and the text file
        return f"""
            <p>Text extracted successfully!</p>
            <p> <a href="{os.path.join(upload_folder, filename)}" download>Download the image</a> </p>
            <p> <a href="{text_output_path}" download>Download the extracted text</a> </p>
        """

    except Exception as e:
        return f"An error occurred while processing the image: {str(e)}"
