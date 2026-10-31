
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 165)

engine.say("Hello! I am Sandarbh's AI. Voice system is working.")
engine.runAndWait()

print("Voice test completed!")
