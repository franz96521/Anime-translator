# -*- coding: utf-8 -*-
import sys , os , time , winsound, wave, shutil , multiprocessing
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
from lib import subtitles as sb
from lib import translate as tr
import vlc
from pathlib import Path


class Window(QMainWindow):
    filename =''
    def __init__(self):
        super().__init__()
        uic.loadUi("AnimeTranslator.ui",self)
        self.setWindowTitle("AnimeTranslator")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('img\icon.png'))
        self.createWindow()

    def createWindow(self):
        self.createStartButton()
        self.ceateMediaPlayer()
        self.addLanguageToTranslate()
        self.progressBar.setValue(0)
      
    def createStartButton(self):
        self.button = QPushButton('Create subtitles')
        self.button.clicked.connect(self.startCreation)
        self.settingsBox.addWidget(self.button)

        self.Video_btn =  QPushButton('select video')
        self.Video_btn.clicked.connect(self.open_file)
        self.videolayout.addWidget(self.Video_btn)


    def ceateMediaPlayer(self):
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.videoframe = QtWidgets.QFrame(
            frameShape=QtWidgets.QFrame.Box, frameShadow=QtWidgets.QFrame.Raised
        )
        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())  
        self.videolayout.addWidget(self.videoframe)

        
        
    def addLanguageToTranslate(self):
        # get list of permitted languages
        
        s = tr.getLanguages()
        #add elements to combo box 
        self.languageOfTheVideo.addItems(s)
        #create language checklist
        column=0                
        vbox = QGridLayout()
        for count, item in enumerate(s): 
            NameId = QCheckBox(item,self)       
            vbox.addWidget(NameId, count//4, column)            
            column+=1
            if column%4==0:
                column=0            
            #NameId.stateChanged.connect(self.handleItemClicked)
        print('languages added')
        # insert language checklist
        self.languageToTranslate.setLayout(vbox)
    # run an create all selected elements 
    

    def startCreation(self):
        self.media.add_options("sub-file={}".format("\\video1\\video1_es.srt"))
        self.progressBar.setValue((100/8)*1)
        file_complete = self.filename
        self.file_name = os.path.basename(os.path.splitext(self.filename)[0])

        original , totranslate =self.getSelectedLanguages()

        x= sb.subtitles()
        self.progressBar.setValue((100/8)*2)
        #extract audio
        audio, rate = x.getaudio(file_complete)              
        path = os.path.splitext(self.filename)[0]
        self.pathOnli = path
        #create path
        self.createFilePath(path)
        self.progressBar.setValue((100/8)*3)
        #save audio         
        shutil.copy(audio, path+'\\'+self.file_name+'.wav')
        self.progressBar.setValue((100/8)*4)
           
        self.progressBar.setValue((100/8)*5)
        #crate final audio
        audio, rate = x.getaudio(path+'\\'+self.file_name+'.wav')
        self.progressBar.setValue((100/8)*6)
        #create captions
        x.generate_subtitles(path,original,0,audio_filename=audio,audio_rate=rate,name=self.file_name)
        self.progressBar.setValue((100/8)*7)
        #translate captions 
        names = tr.translate(totranslate,os.path.splitext(path+'\\'+self.file_name)[0],original)
        self.progressBar.setValue((100/8)*8)
        self.loadwithSubtitles(names)
        


    def createFilePath(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


    def getSelectedLanguages(self):   
        originalLanguage = self.languageOfTheVideo.currentText()
        languagetotranslate=[]
        for checkbox in self.languageToTranslate.findChildren(QtWidgets.QCheckBox):
            if checkbox.isChecked():
                languagetotranslate.append(checkbox.text())
                #print('%s: %s' % (checkbox.text(), checkbox.isChecked()))
        #print(languagetotranslate)
        return originalLanguage , languagetotranslate
   
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        self.filename = filename
        if filename != '':        
            self.media = self.instance.media_new(filename)               
            self.mediaplayer.set_media(self.media)            
            self.mediaplayer.play()
            #self.loadwithSubtitles(names)

    def loadwithSubtitles(self,names):        
        self.media = self.instance.media_new(self.filename)   
        print(names[0])
        self.media.add_options("sub-file={}".format(Path(names[0])))
        self.mediaplayer.set_media(self.media)            
        self.mediaplayer.play()

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())