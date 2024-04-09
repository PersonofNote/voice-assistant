import pyttsx3
import speech_recognition as sr
import webbrowser 
import datetime 
import wikipedia
import sounddevice
from dotenv import load_dotenv


load_dotenv('.env')

# Skills
from skills import *

def init_voice_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
	# TODO: Set a configuration option for this
	# com.apple.speech.synthesis.voice.Cellos is a cool option but very slow
    engine.setProperty('voice', 'com.apple.voice.compact.en-GB.Daniel')
    return engine

default_engine = init_voice_engine()

### Voice Configuration commands
def list_voices(engine = default_engine):
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice.name, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("I'm " + voice.name)
        engine.runAndWait()
        engine.stop()

def takeCommand():

	r = sr.Recognizer()

	with sr.Microphone() as source:
		print('Listening')
		
		# seconds of non-speaking audio before 
		# a phrase is considered complete
		r.pause_threshold = 0.7
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		
		try:
			print("Recognizing")
			#Query = r.recognize_whisper(audio, language='en')
			Query = r.recognize_google(audio, language='en')
			print("Query: ", Query)
			
		except Exception as e:
			print(e)
			print("Say that again please")
			return "None"
		
		return Query

def speak(audio, engine = default_engine):
	engine.say(audio)
	engine.runAndWait()

def Hello():
	speak("Hi")



def Take_query():
	Hello()
	
    # run until exit command is spoken or entered in terminal
	while(True):
		
		query = takeCommand().lower()

		match query:
			case x if "open google" in x:
				speak("Opening Google ")
				webbrowser.open("www.google.com")
			
			case x if "list voices" in x:
				# TODO: add option to set voice
				speak("Listing voices")
				list_voices()

			case x if "shut down" in x:
				speak("Shutting down")
				exit()
			
			case x if "from wikipedia" in x:
				speak("Checking wikipedia ")
				query = query.replace("wikipedia", "")
			
				result = wikipedia.summary(query, sentences=4)
				speak("According to wikipedia")
				speak(result)

			case x if "light" in query:
				# TODO: Clean this up. It's super messy right now. Need a more elegant way to detect the command, and to get the nickname. 
				# But it works for my specific needs
				print("Light based command detected")
				client = wyze_client('./skills/wyze_smartDevices/.env')
				device = wyze_get_mac_from_nickname('bedside', client)
				if "off" in query:
					print("Turning off")
					wyze_execute_command(device, "off", client)
				elif "on" in query:
					print("Turning on")
					wyze_execute_command(device, "on", client)

		'''
		if "open google" in query:
			speak("Opening Google ")
			webbrowser.open("www.google.com")
			continue
		
		# this will exit and terminate the program
		elif "shut down" in query:
			speak("Shutting down")
			exit()
		
		elif "from wikipedia" in query:
			
			speak("Checking wikipedia ")
			query = query.replace("wikipedia", "")
			
			result = wikipedia.summary(query, sentences=4)
			speak("According to wikipedia")
			speak(result)
		'''
		

if __name__ == '__main__':

	Take_query()
