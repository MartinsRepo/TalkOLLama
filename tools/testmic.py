import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    mic = sr.Microphone() # default device index
    with mic as source:
        # r.adjust_for_ambient_noise(source) case you ever have noise issues
        audio = r.listen(source, timeout=10)
        return r.recognize_google(audio)
print(listen())
