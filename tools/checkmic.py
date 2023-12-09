import speech_recognition as sr

for mic in sr.Microphone.list_microphone_names():
    print(mic)


for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
