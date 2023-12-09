import speech_recognition as sr

# Initialize recognizer instance
r = sr.Recognizer()

# Adjust energy threshold for ambient noise level
r.energy_threshold = 4000

# Set dynamic noise threshold (adjust according to your environment)
r.dynamic_energy_adjustment_ratio = 1.3

# Function to listen for audio input from the microphone
def listen_for_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="de-DE")
        return text

    except sr.UnknownValueError:  
        print("Speech not recognized.")

    except sr.RequestError as e:  
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Use the function to capture and recognize speech continuously
while True:
    recognized_text = listen_for_audio()
    
    if recognized_text:
        print(f"Recognized Text: {recognized_text}")