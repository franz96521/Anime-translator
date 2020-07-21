import sys
import os

def splitfiles(source, filename):    
    import warnings
    warnings.filterwarnings('ignore')
    from spleeter.separator import Separator    

    stem = '2stems'
    separator = Separator(f'spleeter:{stem}')
    output_folder = source 
    song = source+'\\'+filename

    separator.separate_to_file(song, output_folder ,synchronous=False)
    separator.join()
    

