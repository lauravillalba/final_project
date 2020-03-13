import os
from pydub import AudioSegment

people = os.listdir("../inputs/LibriSpeech/test-other")

if ".DS_Store" in people:
    people.remove(".DS_Store") 
print(people)

all_files = {}
for p in people:
    list_dir = os.listdir(f'../inputs/LibriSpeech/test-other/{p}')
    if '.DS_Store' in list_dir:
        list_dir.remove(".DS_Store")
    file_dict ={}
    for l in list_dir:
        files = [x for x in os.listdir(f'../inputs/LibriSpeech/test-other/{p}/{l}') if x.endswith(".flac")]
        file_dict[l]= files
    
    all_files[p] = file_dict

#Unifico audios por persona y cambio a formato MP3:
for p_id, p_info in all_files.items():
    audio = 0
    for key, values in p_info.items():
        for v in values:
            audio += AudioSegment.from_file(f'../inputs/LibriSpeech/test-other/{p_id}/{key}/{v}', format = 'flac')
    
    audio.export(f'../outputs/combined_sound/{p_id}.mp3', format='mp3')
    
# Analizo los audios, para descartar aquellos con time <600000 para que el resultado final quede balanceado.
milis=6000000000
time = []
for p in people:
    origin = AudioSegment.from_file(f'../outputs/combined_sound/{p}.mp3', format='mp3')
    time.append((p,len(origin)))
    if len(origin)<milis:
        milis=len(origin)

discarted = [e[0] for e in time if e[1]<600000]
print('Descartados: ',discarted)

#Audios 20' y overlap 50%:
for p in people:
    if p not in discarted:
        interval = 20000
        origin = AudioSegment.from_file(f'../outputs/combined_sound/{p}.mp3', format='mp3')
        num = (len(origin)//interval)*2
        print(num)
        counter = 0

        for i in range(num):
            if counter == 0:
                splited = origin[0:interval]
                counter+=int(interval/2)
                interval+=int(counter)
            else: 
                splited = origin[counter:interval]
                counter+=10000
                interval+=10000

            splited.export(f'../outputs/splited_audio/{p}_{i}.mp3', format='mp3')
            print(f'Exportado {p}_{i}.mp3 - audio_time= {len(splited)}')
    else: 
        print(p, 'Descartado!')


print('FIN! Todos los audios están en ../outputs/splited_audio/')