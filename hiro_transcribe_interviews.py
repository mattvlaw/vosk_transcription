#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json
import glob
from tqdm import tqdm

SetLogLevel(0)

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)




model = Model("model")

def transcribe_wav(full_filename):
    wf = wave.open(full_filename, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)
    
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    # get the filename from the path without the extension
    filename = os.path.join('transcripts',os.path.splitext(os.path.basename(full_filename))[0] + ".txt")

    with open(filename, 'w+') as f:
        line_no = 0
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                
                line = json.loads(rec.Result())["text"]
                f.write(line + "\n")
                print(f"Wrote line {line_no} to {filename}")
                line_no += 1
                
            else:
                # print(json.loads(rec.PartialResult()))
                pass
        f.write(json.loads(rec.FinalResult())["text"])

if __name__=='__main__':
    # use glob to get all the wav files in the current folder
    filenames = glob.glob("interview_audio/*.wav")
    filenames.sort()
    print(filenames)
    for f in tqdm(filenames):
        transcribe_wav(f)

    print("finished")
