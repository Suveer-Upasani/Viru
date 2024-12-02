from PIL import Image
import pytesseract
import os

def process_image_and_save_text(image_file, upload_folder):
    try:
        # Save the image to the server
        filename = image_file.filename
        file_path = os.path.join(upload_folder, filename)
        image_file.save(file_path)

        # Open the image and verify if it's valid
        try:
            image = Image.open(file_path)  # Open the image to verify it's valid
            image.verify()  # Verify that it's a valid image file
        except (IOError, SyntaxError) as e:
            return f"Invalid image file. Error: {str(e)}"

        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image, lang="eng")

        # Define the output text file path
        text_output_path = os.path.join(upload_folder, f"{filename}_extracted.txt")

        # Save the extracted text to a text file
        with open(text_output_path, 'w') as output_file:
            output_file.write(extracted_text)

        # Return the result with the path to the saved text
        return f"Text extracted successfully. <a href='{text_output_path}'>Download the text file</a>"

    except Exception as e:
        return f"An error occurred while processing the image: {str(e)}"
