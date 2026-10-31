
import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise RuntimeError("ELEVENLABS_API_KEY is missing from .env")

audio_file = Path("voice/jarvis_voice.mp3")

if not audio_file.exists():
    raise FileNotFoundError(
        f"Voice recording not found: {audio_file}"
    )

client = ElevenLabs(api_key=api_key)

print("Creating your custom JARVIS voice...")

with audio_file.open("rb") as audio:
    voice = client.voices.ivc.create(
        name="Sandarbh JARVIS",
        description="Custom authorized JARVIS-style assistant voice",
        files=[audio]
    )

print("\nVoice created successfully!")
print("Voice ID:", voice.voice_id)
print("\nSave this ID. We need it for OpenJarvis.")
