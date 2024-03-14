### Not imported right now. Need to resolve the circular default engine requirements, 
### or else pass in an engine to everything everywhere all the time
import pyttsx3

def init_voice_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
	# 0 is male voice, 1 is female voice
    # engine.setProperty('voice', voices[0].id)
    return engine

def list_voices(engine):
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("Hello World!")
        engine.runAndWait()
        engine.stop()

