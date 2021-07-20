####################################
###                              ###
###        PARLA GSR v0.32       ###
###                              ###
###==============================###
### by Davi Ramalho - 2021.05.05 ###
####################################

# Import Libraries

import os
import subprocess
import speech_recognition as sr

# Extract Audio from Video (MP4)

command = "ffmpeg -i video.mp4 -f mp3 -ab 192000 -vn audio.mp3"
subprocess.call(command, shell=True)
command = "ffmpeg -i audio.mp3 -acodec pcm_s16le -ac 1 -ar 16000 audio_wav.wav"
subprocess.call(command, shell=True)

# Split Audio
# Don't forget to install ffmppeg on local machine

command = "ffmpeg -i audio_wav.wav -f segment -segment_time 180 -c copy %03d.wav"
subprocess.call(command, shell=True)

# Colect WAV files

files = []
for filename in os.listdir("."):
    if filename.endswith(".wav") and filename != "audio_wav.wav":
        files.append(filename)
files.sort()

# Speech to Text Recognition by Google
# Language: pt-BR

results = []
for filename in files:
    with open(filename, "rb") as f:
        r = sr.Recognizer()
        audio_test = sr.AudioFile(f)
        with audio_test as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
        res = r.recognize_google(audio, language='pt-BR')
        results.append(res)

# Colect Text

text = []
for result in results:
    text.append(result + ".\n")

# Print to check

print(text)

# Write out .txt file

with open("output.txt", "w") as out:
    out.writelines(text)
