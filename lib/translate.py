# -*- coding: utf-8 -*-
import io , os
import time
import googletrans
from googletrans import Translator

translator = Translator(service_urls=['translate.google.com'])

def getLanguages():
	ls = list(googletrans.LANGUAGES)
	ls.sort()
	return ls

def translate_text(text, target,src):
	result = translator.translate(text,src=src, dest=target)
	return result.text

def translate(languages, filename ='', origin=''):		
	names = []
	names.append(filename + ".srt")
	for lang in languages:
		time.sleep(15)
		with io.open(filename + "_" + lang + ".srt",'wb') as translate_file:
			with io.open(filename + ".srt",'r',encoding='utf8') as original_file:
				names.append(filename + "_" + lang + ".srt")
				contents = original_file.readlines()
				contents[0] = "1\n"
				for i in range(len(contents)):	
					if i%200==0:
						translator = None
						#time.sleep(15)
						translator = Translator(service_urls=['translate.google.com'])
					if contents[i][0].isdigit() or contents[i][0]=="\n":
						translate_file.write(contents[i].encode())						
					else:
						receive = translate_text(contents[i],lang,origin)			
						print(receive) 
						translate_file.write((receive + "\n").encode())

	
	return names 
						
						


