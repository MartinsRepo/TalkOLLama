import speech_recognition as sr
from vosk import Model, KaldiRecognizer

# Initialize recognizer instance
r = sr.Recognizer()

# Load the Vosk model and create a recognizer object
model = Model("..\\languagemodels\\vosk-model-small-de-0.15")
rec = KaldiRecognizer(model, 16000)

# Function to listen for audio input from the microphone and recognize speech using Vosk
def listen_for_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        
        # Get the raw audio data from SpeechRecognition's AudioData class
        raw_audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)

    try:
        # Pass the raw audio data to Vosk recognizer instead of Google Speech Recognition API 
        rec.AcceptWaveform(raw_audio_data)
    
        # Retrieve recognized text from Vosk recognizer
        result = rec.Result()
        
        return result
        
    except sr.UnknownValueError:  
        print("Speech not recognized.")

    except sr.RequestError as e:  
         print(f"Could not request results; {e}")

# Use the function to capture and recognize speech continuously       
while True:
    recognized_result = listen_for_speech()
    
    if recognized_result:
         print(f"Recognized Text: {recognized_result}")