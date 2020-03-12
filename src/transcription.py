import speech_recognition as sr
from os import path
from pydub import AudioSegment

def transcripAudio(splitedAudio):
    # MP3 a WAV para poder aplicar la recognize_google:                                                       
    #sound = AudioSegment.from_file(mp3, format = 'mp3')
    sound = splitedAudio.set_frame_rate(8000)
    sound.export("../outputs/transcript/transcript.wav", format="wav")

    # transcribe audio file                                                         
    AUDIO_FILE = "../outputs/transcript/transcript.wav"

    # use the audio file as the audio source                                        
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file                  
            try:
                #print("Transcription: ", r.recognize_google(audio))
                return r.recognize_google(audio)
            except sr.UnknownValueError:
                #print("Google Speech Recognition could not understand audio")
                return "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                #print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return "Could not request results from Google Speech Recognition service; {0}".format(e)
