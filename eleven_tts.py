
import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise RuntimeError("ELEVENLABS_API_KEY is missing from .env")

client = ElevenLabs(api_key=api_key)


def speak(text):
    """Generate speech using an ElevenLabs AI voice."""

    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
    )

    output = Path("jarvis_response.mp3")

    with output.open("wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Speech saved to {output}")


if __name__ == "__main__":
    speak("Hello! I am Sandarbh's AI. How can I help you today?")
