import json
from pydub import AudioSegment
from scipy.fftpack import fft
import sys

people_mix = sys.argv

print(f'Generando audio...{people_mix}')

speakers = []
audio_original = 0
for p in people_mix[2:]:
    speakers.append(p.split('_')[0])
    audio_original += AudioSegment.from_file(f"../outputs/splited_audio/{p}.mp3", format='mp3')

audio_original.export(f"../outputs/audioMix/{people_mix[1]}.mp3", format="mp3")

print(f'Se ha guardado el audio {people_mix[1]}.mp3 --> ../outputs/audioMix')
print(f'En este audio hablan: {list(set(speakers))}')

