import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment

from vosk import GpuThreadInit, Model, KaldiRecognizer, GpuInit
import json
import wave
import Word as custom_Word
import os
os.add_dll_directory(os.getcwd())
import vlc
import time


MP4_PATH = "C:/Users/david/Documents/media/video.mp4"
MP3_PATH = "C:/Users/david/Documents/media/video.mp3"
WAV_PATH = "C:/Users/david/Documents/media/video.wav"
MONO_WAV_PATH = "C:/Users/david/Documents/media/video_mono.wav"
SHORT_WAV_PATH = "C:/Users/david/Documents/media/short_video"
TXTOUT_PATH = "C:/Users/david/Documents/media/video_text.txt"
JSON_PATH = "C:/Users/david/Documents/media/video_json.txt"

def main():
    cut_audio()
    # KEYWORD = input('keyword: ')
    # if (not os.path.exists(MP3_PATH)):
    #     convert()
    # if not os.path.exists(SHORT_WAV_PATH):
    #     cut_audio()
    # value = input('choose function: ')
    # if value == 't':
    #     if os.path.exists(JSON_PATH):
    #         os.remove(JSON_PATH)
    #     open(JSON_PATH, 'w')
    #     vosk_rec_thorough()
    #     player()
    # elif value =='n':
    #     player()


# Conversion from mp4 to mp3 and then top mp3 to wav, then to mono channel wav
def convert():
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP4_PATH, output=MP3_PATH)
    ffmpeg_tools.ffmpeg_extract_audio(inputfile=MP3_PATH, output=WAV_PATH)
    sound = AudioSegment.from_wav(WAV_PATH)
    sound = sound.set_channels(1)
    sound.export(MONO_WAV_PATH, format="wav")

# get short part of audio
def cut_audio():
    audio = AudioSegment.from_wav(MONO_WAV_PATH)
    nb_frames = audio.frame_count()
    part_length = float(nb_frames/8)
    print(part_length)
    short_audio=[]
    j =0
    # for i in range(0,8):
    #     cut = audio[((i)*part_length):((i+1)*part_length)]
    #     print(cut.frame_count())
    #     short_audio.append(cut)
    #     cut.export(SHORT_WAV_PATH+str(j)+".wav", format='wav')
    #     j = j+1
    for el in audio.dice(audio.duration_seconds/8):
        el.export(SHORT_WAV_PATH+str(j)+".wav", format='wav')
        j = j+1

def vosk_rec_thorough():
    # GpuInit()
    # GpuThreadInit()
    wf = wave.open(MONO_WAV_PATH, "rb")
    results = []
    textResults = []
  

    model = Model(r"C:/Users/david/Documents/media/vosk-model-en-us-0.22")

    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            part_result = json.loads(recognizer.Result())
            results.append(part_result)

    part_result = json.loads(recognizer.FinalResult())
    results.append(part_result)
    list_of_Words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = custom_Word.Word(obj)  # create custom Word object
            list_of_Words.append(w)  # and add it to list
    # write results to a file
    for word in list_of_Words:
        print(word.to_string())
        with open(JSON_PATH, 'a+') as output:
            print(word.to_txt(), file=output)

    with open(JSON_PATH_1, 'w') as output:
        print(results, file=output)

   

    # write text portion of results to a file
    with open(TXTOUT_PATH_1, 'w') as output:
        print(json.dumps(textResults, indent=4), file=output)
    # write text portion of results to a file
    # with open(TXTOUT_PATH, 'w') as output:
    #     print(json.dumps(textResults, indent=4), file=output)

main()