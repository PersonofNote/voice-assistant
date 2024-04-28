#!/home/jessicamartin/Documents/voice_assistant/.venv/bin/python


import pyttsx3
import speech_recognition as sr
import webbrowser 
import datetime 
import wikipedia
import sounddevice
from dotenv import load_dotenv
from pocketsphinx import LiveSpeech

load_dotenv('.env')

# Skills
from skills import *

# init variables
wyze_client = wyze_client('.env')

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

def takeCommand(r, mic):

	with mic as source:
		print('Listening')
		
		# seconds of non-speaking audio before 
		# a phrase is considered complete
		r.pause_threshold = 0.5
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		
		try:
			print("Recognizing")
			#Query = r.recognize_whisper(audio, language='en')
			Query = r.recognize_google(audio, language='en')
			# Query = r.recognize_sphinx(audio, language='en')
			print("Query: ", Query)

		except sr.UnknownValueError:
			print("Speech recognition could not understand audio")
			return "None"
		except sr.RequestError as e:
			print(f"Request error: {e}")
			return "None"
		
		return Query

def speak(audio, engine = default_engine):
	engine.say(audio)
	engine.runAndWait()

def Hello():
	speak("Voice assistant running")

def initializeRecognizer():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    return recognizer, microphone



def Take_query():
	Hello()
	recognizer, microphone = initializeRecognizer()

	wakeword = False
	for phrase in LiveSpeech():
		if phrase.contains('computer'): wakeword = True
		print(phrase.contains('computer'))
		return wakeword
	

    # run until exit command is spoken or entered in terminal
	while(True):
		query = takeCommand(recognizer, microphone).lower()

		match query:			
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

			case x if "turn" in query:
				# TODO: Clean this up. It's super messy right now. Need a more elegant way to detect the command, and to get the nickname.
				# Probably to initialize the client, 
				# But it works for my specific needs
				print("Light based command detected")
				stopwords = ['turn', 'off', 'on']
				q = query.lower().split()
				device_nickname = " ".join(filter_arr(q, stopwords))
				print(device_nickname)
				try:
					device = wyze_get_mac_from_nickname(device_nickname, wyze_client)
					if "off" in query:
						print("Turning off")
						wyze_execute_command(device, "off", wyze_client)
					elif "on" in query:
						print("Turning on")
						wyze_execute_command(device, "on", wyze_client)
				except Exception as e:
					print(e)
					return "None"
				
			case x if "food info" in query:
					file_path = './data/foodkeeper.json'
					q = query.lower().split()
					stopwords = read_stopwords('./data/stopwords.txt')
					filtered_query = filter_arr(q, stopwords)
					search_keyword = filter_arr(filtered_query, ['food', 'info'])
					fields_to_return = ['refrigerate_after_opening_max']

					print(filtered_query)
					print(search_keyword)

					search_results = search_food_json(file_path, search_keyword, fields_to_return)

					if search_results:
						for result in search_results:
							print(result)
					else:
						print("No matching items found.")


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
