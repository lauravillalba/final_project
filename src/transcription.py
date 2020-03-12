import speech_recognition as sr
from os import path
from pydub import AudioSegment

# convert mp3 file to wav                                                       
sound = AudioSegment.from_file("../src/transcription3.aiff", format = 'aiff')
sound.export("transcript.wav", format="wav", parameters=["-ar", "8000"])
#sound = AudioSegment.from_file("transcript.wav", format="wav", frame_rate=16000)
#sound.export("transcript.wav", format="wav", parameters=["-ar", "8000"])

# transcribe audio file                                                         
AUDIO_FILE = "transcript.wav"

# use the audio file as the audio source                                        
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file                  
        try:
            print("Transcription: ", r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
