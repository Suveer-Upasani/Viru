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
    file_path = os.path.join('uploads', filename)

    # Detect file encoding
    with open(file_path, 'rb') as fh:
        raw_data = fh.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding'] or 'utf-8'  # Use utf-8 if encoding not detected

    # Read the file content
    try:
        with open(file_path, "r", encoding=encoding) as fh:
            my_text = fh.read().replace("\n", " ")
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="ISO-8859-1") as fh:
            my_text = fh.read().replace("\n", " ")

    # Log the text read
    print(f"Text read from file: {my_text[:200]}...")  # Show first 200 chars for brevity

    # Map language name to language code
    lang_code = LANGUAGE_CODES.get(language)
    if not lang_code:
        raise ValueError(f"Language not supported: {language}")

    # Convert text to speech
    tts = gTTS(text=my_text, lang=lang_code, slow=False)

    # Ensure 'outputs' directory exists
    if not os.path.exists('outputs'):
        os.makedirs('outputs')  # Create folder if it doesn't exist

    # Save the audio file to 'outputs' folder
    output_path = os.path.join('outputs', 'output.mp3')
    tts.save(output_path)

    # Play the audio file
    playsound(output_path)

    return f"Audio successfully created and played: {output_path}"
