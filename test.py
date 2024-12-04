# from gtts import gTTS
# import os
# import chardet
# from playsound import playsound

# # Language mapping
# LANGUAGE_CODES = {
#     "English": "en",
#     "French": "fr",
#     "Spanish": "es",
#     "German": "de",
#     "Chinese": "zh-CN",
#     "Marathi": "mr",
#     "Hindi": "hi",
# }

# def run_test(filename, language):
#     try:
#         # Paths for file storage
#         upload_dir = 'uploads'
#         output_dir = 'outputs'
#         file_path = os.path.join(upload_dir, filename)

#         # Check if the file exists
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"File not found: {file_path}")

#         # Detect file encoding
#         with open(file_path, 'rb') as fh:
#             raw_data = fh.read()
#             result = chardet.detect(raw_data)
#             encoding = result['encoding'] or 'utf-8'  # Fallback to UTF-8

#         # Read the file content
#         try:
#             with open(file_path, "r", encoding=encoding) as fh:
#                 my_text = fh.read().replace("\n", " ")
#         except UnicodeDecodeError:
#             # Fallback encoding
#             with open(file_path, "r", encoding="ISO-8859-1") as fh:
#                 my_text = fh.read().replace("\n", " ")

#         # Map language name to language code
#         lang_code = LANGUAGE_CODES.get(language)
#         if not lang_code:
#             raise ValueError(f"Language not supported: {language}")

#         # Convert text to speech
#         output = gTTS(text=my_text, lang=lang_code, slow=False)

#         # Ensure output directory exists
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)

#         # Save the audio file
#         output_path = os.path.join(output_dir, 'output.mp3')
#         output.save(output_path)

#         # Play the audio file
#         playsound(output_path)

#         return f"Audio successfully created and played: {output_path}"

#     except FileNotFoundError as e:
#         return f"Error: {e}"

#     except ValueError as e:
#         return f"Error: {e}"

#     except Exception as e:
#         return f"An unexpected error occurred: {e}"


from gtts import gTTS
import os
import chardet
from playsound import playsound

# Language mapping
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh-CN",
    "Marathi": "mr",
    "Hindi": "hi",
}

def run_test(filename, language):
    try:
        # Paths for file storage
        upload_dir = 'uploads'
        output_dir = 'outputs'
        file_path = os.path.join(upload_dir, filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Detect file encoding
        with open(file_path, 'rb') as fh:
            raw_data = fh.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'  # Fallback to UTF-8

        # Read the file content
        try:
            with open(file_path, "r", encoding=encoding) as fh:
                my_text = fh.read().replace("\n", " ")
        except UnicodeDecodeError:
            # Fallback encoding
            with open(file_path, "r", encoding="ISO-8859-1") as fh:
                my_text = fh.read().replace("\n", " ")

        # Map language name to language code
        lang_code = LANGUAGE_CODES.get(language)
        if not lang_code:
            raise ValueError(f"Language not supported: {language}")

        # Convert text to speech
        output = gTTS(text=my_text, lang=lang_code, slow=False)

        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the audio file
        output_path = os.path.join(output_dir, 'output.mp3')
        output.save(output_path)

        # Play the audio file
        playsound(output_path)

        return f"Audio successfully created and played: {output_path}"

    except FileNotFoundError as e:
        return f"Error: {e}"

    except ValueError as e:
        return f"Error: {e}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"
