# -*- coding: utf-8 -*-
import subtitles as sb
import translate as tr
import multiprocessing

import time
import os
import winsound
import wave
import shutil
import sp
#source= r'C:\Users\franz\OneDrive\Documentos\GitHub\anime translator\media\audio\vocals\vocal4.wav'
source= r'C:\Users\franz\OneDrive\Documentos\GitHub\anime translator\media\video\mitos zoologicos.mp4'
origin ='es'
translation = 'en'


if __name__ == '__main__':
    
    multiprocessing.freeze_support()
    x= sb.subtitles()
    audio, rate = x.getaudio(source)
    del x
    file_name = os.path.basename(os.path.splitext(source)[0])
    print(file_name)
    path = os.path.splitext(source)[0]+''   

    if not os.path.exists(path):
        os.makedirs(path)
    shutil.copy(audio, path+'\\'+file_name+'.wav')
    
    y= sp.splitfiles(path,file_name+'.wav') 
    del y
    x= sb.subtitles()
    audio, rate = x.getaudio(path+'\\'+file_name+'\\vocals.wav')
    #winsound.PlaySound(audio, winsound.SND_FILENAME) 
    
    x.generate_subtitles(path,origin,0,audio_filename=audio,audio_rate=rate,name=file_name)
    del x
    print('\n')
    tr.translate(translation,os.path.splitext(path+'\\'+file_name)[0],origin)

    
    