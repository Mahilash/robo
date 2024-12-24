import requests
import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment

def generate_content(prompt):
    """Generate content using the Gemini API."""
    api_key = "AIzaSyBRt4jRf2xyRqmXOhlnm3xN3DECSAd3bOI"  
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        generated_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return generated_text
    else:
        return None

def text_to_speech(text):
    """Convert text to speech and play it using pyttsx3 engine."""
    engine = pyttsx3.init()
    engine.say(text)  
    engine.runAndWait()

def speech_to_text(audio_file):
    """Convert audio to text using speech_recognition."""
    recognizer = sr.Recognizer()

    if audio_file.filename.endswith('.mp3'):
        audio_file_path = "temp_audio.wav"
        audio = AudioSegment.from_mp3(audio_file)
        audio.export(audio_file_path, format="wav")
    elif audio_file.filename.endswith('.wav'):
        audio_file_path = audio_file
    else:
        return None  

    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def main():
    recognizer = sr.Recognizer()

    while True:
        print("Listening for your input...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized speech: {text}")
            response = generate_content(text)
            if response:
                print(f"Generated response: {response}")
                
                text_to_speech(response)
            else:
                print("Sorry, there was an error generating content.")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the speech. Please try again.")
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")

if __name__ == "__main__":
    main()
