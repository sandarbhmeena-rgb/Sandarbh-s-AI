
import speech_recognition as sr
import pyttsx3
import tempfile
from pathlib import Path


def speech_to_text(audio_bytes):
    """Convert microphone recording into text."""

    recognizer = sr.Recognizer()

    try:
        import io

        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        return text, None

    except sr.UnknownValueError:
        return None, "I couldn't understand your voice. Try again."

    except sr.RequestError:
        return None, "Speech recognition requires internet."

    except Exception as error:
        return None, str(error)


def text_to_speech(text):
    """Generate spoken AI response."""

    try:
        engine = pyttsx3.init()

        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        audio_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        audio_path = audio_file.name
        audio_file.close()

        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        engine.stop()

        if Path(audio_path).exists():
            if Path(audio_path).stat().st_size > 0:
                return audio_path, None

        return None, "Audio generation failed."

    except Exception as error:
        return None, str(error)
