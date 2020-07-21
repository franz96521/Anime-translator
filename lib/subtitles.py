import autosub
from autosub import FLACConverter
from autosub import SpeechRecognizer
from autosub import extract_audio
from autosub import find_speech_regions
from autosub import DEFAULT_CONCURRENCY
from autosub import DEFAULT_SUBTITLE_FORMAT
from autosub import GOOGLE_SPEECH_API_KEY
from autosub.formatters import FORMATTERS

import multiprocessing
import time
import os
import winsound

class subtitles():
    @staticmethod
    def getaudio(source_path):
        audio_filename, audio_rate = extract_audio(source_path)       
        return audio_filename, audio_rate

    @staticmethod
    def generate_subtitles(
            source_path,
            src_language,
            listener_progress,
            output=None,
            concurrency=DEFAULT_CONCURRENCY,
            subtitle_file_format=DEFAULT_SUBTITLE_FORMAT,
            audio_filename='',
            audio_rate='',
            name=''
        ):      

        

        regions = find_speech_regions(audio_filename)

        converter = FLACConverter(source_path=audio_filename)
        recognizer = SpeechRecognizer(language=src_language, 
                                        rate=audio_rate,
                                        api_key=GOOGLE_SPEECH_API_KEY)
        transcripts = []
        if regions:
            try: 
                print("Step 1 of 2: Converting speech regions to FLAC files ")
                len_regions = len(regions)
                extracted_regions = []

                subtitles.pool = multiprocessing.Pool(concurrency)
                for i, extracted_region in enumerate(subtitles.pool.imap(converter, regions)):                    
                    extracted_regions.append(extracted_region)
                    print(i)
                  
                subtitles.stop()

                print("Step 2 of 2: Performing speech recognition ")
                subtitles.pool = multiprocessing.Pool(concurrency)
                for i, transcript in enumerate(subtitles.pool.imap(recognizer, extracted_regions)):                   
                    transcripts.append(transcript)
                    print(i)       
                subtitles.stop()
               
                

            except KeyboardInterrupt:
                subtitles.pbar.finish()
                subtitles.stop()
                raise

        timed_subtitles = [(r, t) for r, t in zip(regions, transcripts) if t]
        formatter = FORMATTERS.get(subtitle_file_format)
        formatted_subtitles = formatter(timed_subtitles)

        dest = output

        if not dest:
            base = os.path.splitext(source_path)[0]+'\\'+name
            dest = "{base}.{format}".format(base=base, format=subtitle_file_format)

        with open(dest, 'wb') as output_file:
            output_file.write(formatted_subtitles.encode("utf-8"))

        os.remove(audio_filename)

        subtitles.stop()
        return dest

    @staticmethod
    def stop():
        subtitles.pool.close()
        subtitles.pool.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()