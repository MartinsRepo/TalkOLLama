################################################################
# File: talkollama.py
# Purpose:
# - voice detection via microphone
# - Q/A to a local Large Language Model
# - Voice output
# - no internet access necessary
#
# Licence: Apache 2.0
#
# Martin Hummel
# 12.12.2023
################################################################


from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from vosk import Model, KaldiRecognizer
from vosk import SetLogLevel
SetLogLevel(-1)
from langchain.chains import RetrievalQA


import os
import sys
import argparse
from contextlib import contextmanager
import threading

# listen
import speech_recognition as sr

# talk
import pydub
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from gtts.tokenizer.pre_processors import abbreviations, end_of_line
from pygame import mixer
import time
import jsons
import re

from PyQt5.QtCore import QObject, pyqtSignal

class LogEmitter(QObject):
    log_signal = pyqtSignal(str)
    
    
# gTTS audio output
audio_settings = {
        "sample_rate": 22050,  	# Higher sample rate improves audio quality
        "channels": 2,  	# Stereo sound provides a fuller hearing experience
        "format": "wav"  	# WAV format supports higher bitrate for better audio quality
    }
    

class AiTalk:
	# Add a LogEmitter instance
	log_emitter = LogEmitter()
	
	def __init__(self, model, lang):
		self.model = model
		self.lang = lang
		self.chat_model_response = None
		self.template = ""
		
		# here you can add your preferred language. Don't forget to download the corresponding language model from VOSK
		if self.lang == 'de':
			self.prompt = PromptTemplate(
			    template="""/
				Du bist ein Assistent und beantwortest nur die Fragen des Benutzers auf Deutsch in kompakter Form. /
				Frage: {question}. Antworte in maximal 2 Sätzen und dann Stop. Antwort: """,
			    input_variables=["question"]
			)	
		elif self.lang == 'en':
			self.prompt = PromptTemplate(
			    template="""/
				You are a chatbot assistant and you are answering to the user questions in english by compact sentences. /
				Question: {question}. Answer in maximal two sentences and then wait. Answer: """,
			    input_variables=["question"]
			)
		
		self.log_emitter.log_signal.emit('Initialisation done\n')
			

	def initSoundystem(self):
		text='Language selected: '+self.lang
		self.log_emitter.log_signal.emit(text)
		self.log_emitter.log_signal.emit('Initialising Vosk. ** Please wait a moment **\n')
		if self.lang == 'de':
			#VOSK speech model
			self.listenmodel = Model("./languagemodels/vosk-model-de-0.21", lang="de-DE")		
		elif self.lang == 'en':
			#VOSK speech model
			self.listenmodel = Model("./languagemodels/vosk-model-en-us-0.22", lang="en-US")

		
		self.rec = KaldiRecognizer(self.listenmodel, 16000)
		
		self.sr = sr
		self.mic = sr.Microphone() 
		self.recog = sr.Recognizer()
		self.mixer = mixer
		self.mixer.init()
		
		# Add a threading event to control the AI processing
		self.stop_event = threading.Event()
	

	def extract_string(self,string):
		# Validate the JSON string
		json_object = jsons.dumps(string, indent = 4) 
	 
		json_data = jsons.loads(json_object)
		
		return json_data["kwargs"]["content"]


	def audioTalk(self, speak, ffile):
		mp3_fp = BytesIO()

		speak.write_to_fp(mp3_fp)

		mp3_fp.seek(0)
		audio = AudioSegment.from_mp3(mp3_fp)

		# Resample the audio to the desired sample rate
		audio = audio.set_frame_rate(audio_settings["sample_rate"])

		# Apply noise reduction to improve audio clarity
		audio = audio.apply_gain(-10)  # Reduce background noise by 10 dB

		# Save the optimized audio file
		audio.export(ffile, format=audio_settings["format"])

		self.mixer.music.load(ffile)
		self.mixer.music.play()  # Wait for the audio to be played
		os.remove(ffile)
	

	def sayListening(self):
		time.sleep(1)
		print('Start listening ...\n')
		self.log_emitter.log_signal.emit('Start listening ...\n')
		if self.lang == 'de':
			text = 'Fertig, ich höre'
		elif self.lang == 'en':
			text = 'Ready, I am listening'		
	  
		speak = gTTS(text=text, lang=self.lang, slow=False) 
		self.audioTalk(speak,'start.wav')
		time.sleep(2)
  

	def answer(self):
		
		json_string = self.chat_model_response.to_json()
		
		extracted_answer = self.extract_string(json_string)
		self.log_emitter.log_signal.emit(extracted_answer)
				
		speak = gTTS(extracted_answer, lang=self.lang, slow=False, pre_processor_funcs = [abbreviations, end_of_line]) 
		self.audioTalk(speak, 'answer.wav')
		
		time.sleep(int(len(extracted_answer)*0.1))
	
	
	def voidAnswer(self):
		if self.lang == 'de':
			speak = gTTS("Ich habe die Frage nicht verstanden", lang=self.lang, slow=False, pre_processor_funcs = [abbreviations, end_of_line]) 
		elif self.lang == 'en':
			speak = gTTS("I didn't understand your question", lang=self.lang, slow=False, pre_processor_funcs = [abbreviations, end_of_line]) 
		self.audioTalk(speak, 'optimized_output.wav')
		time.sleep(2)


	def get_voice_input(self):

		with self.mic as source:
			
			self.sayListening()
			
			# Adjust energy threshold for ambient noise level
			self.recog.energy_threshold = 4000

			# Set dynamic noise threshold (adjust according to your environment)
			self.recog.dynamic_energy_adjustment_ratio = 1.3
			
			self.recog.adjust_for_ambient_noise(source)
			
			print("Listening...")
			audio = self.recog.listen(source)

			try:
				# Get the raw audio data from SpeechRecognition's AudioData class
				raw_audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
				# Pass the raw audio data to Vosk recognizer instead of Google Speech Recognition API 
				self.rec.AcceptWaveform(raw_audio_data)

				# Retrieve recognized text from Vosk recognizer
				question = self.rec.Result()
				
				match = re.search(": \"", question)

				query = ""
				if match:
					query = match.string
					query=query[13:len(query)-1]
					
				if query == "":
					query = ""

				self.log_emitter.log_signal.emit(f"You said: {query}")
				
				return query
			
			except self.sr.UnknownValueError:
				self.log_emitter.log_signal.emit("Sorry, I could not understand your voice.")
				return None
			
			
		return None


	def aiprocess(self):

		print('Model loading ...', self.model)

		chat_model = ChatOllama(
					model=self.model,
					language=self.lang,
					callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
					verbose=False,
					llm_kwargs={"max_length": 4096},
		                	temperature=0.5,
		                	n_ctx=1000.0,
		                	top_k = '30',
		                	repeat_penalty = '1.2',	
		)
		
		self.initSoundystem()
		
		while not self.stop_event.is_set():
			question = ""
			question = self.get_voice_input()
			print(question)

			if question:
				if question.lower() in ["quit", "exit", "stop"]:
					self.stop_event.set()
					break
				
				modified_prompt: str = self.prompt.format(question=question)

				messages = [
					HumanMessage(
						content=question
					)
				]

				self.chat_model_response = chat_model(messages)

				self.answer()
			else:
				self.voidAnswer()

		print('Session stopped - please restart')


	def stop_aiprocess(self):
		# Method to set the stop event, terminating the AI processing loop
		self.stop_event.set()


	
