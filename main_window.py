from json.tool import main
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir, Qt, QUrl, QThreadPool, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QHBoxLayout, QVBoxLayout,
                            QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QWidget, QAction)
from PyQt5.QtGui import QIcon

from qt_material import apply_stylesheet
import datetime
import sys
import os
import pickle

#Data Collection Worker
from sampling_worker import DataCollectWorker

class mainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(mainWindow, self).__init__()
        self.timer = QTimer()
        self.timer.setInterval(1000) #1000s
        self.current_session_seconds = 0
        self.threadpool = QThreadPool()


        # #Thread
        # data_worker = DataCollectWorker()
        

        self.setWindowTitle('EEG Sampling App')
        self.sc = QWidget()
        self.sc.setStyleSheet("background-color: black")
        self.setCentralWidget(self.sc)
        #Add Horizontal layout
        self.container = QVBoxLayout()
        self.container.setContentsMargins(0,0,0,0)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.stateChanged.connect(self.onMediaStateChanged)
        self.media_played = False

        #Start
        self.startUi()
        self.sw = 0


    #ui related ----------------------------------------------------------
    def startUi(self):
        #button at buttom and empty black screen
        start_btn = QPushButton('Start Recording Sequece')
        start_btn.setEnabled(True)
        start_btn.setProperty('class', 'danger')
        start_btn.resize(150, 50)
        start_btn.clicked.connect(self.onStartBtnClicked) 

        self.container.addStretch()
        self.container.addStretch()
        self.container.addStretch()
        self.container.addWidget(start_btn)
        self.sc.setLayout(self.container)

    def readyUi(self):
        pass

    def cueImageUi(self):
        pic = QLabel()
        # pic.setPixmap(QtGui.QPixmap("cue.png"))
        pic.setText('Cue')
        pic.setAlignment(Qt.AlignCenter)
        pic.show()

        self.container.addStretch()
        self.container.widget(pic)
        self.container.addStretch()
        self.sc.setLayout(self.container) 

    def actionObserveUi(self):
        action_obersve_video = QVideoWidget()
        self.media_player.setVideoOutput(action_obersve_video)
        
        #change random action here
        self.media_player.setMedia(QMediaContent(QUrl('cat.mp4')))
        self.container.widget(action_obersve_video)
        
        self.media_player.play()
        self.sc.setLayout(self.container) 
        

    def dataSamplingUi(self):
        #clear everything
        pass 

    def newSessionIndicateUi(self):
        #count down with text
        self.inform_text = QLabel()
        self.container.addStretch()
        self.container.widget(self.inform_text)
        self.container.addStretch()
        self.sc.setLayout(self.container) 
    
    def clearUi(self):
        print(self.container.count)
        for i in reversed(range(self.container.count())): 
            self.container.itemAt(i).widget().setParent(None)
        
    #Callback----------------------------------------------------------
    def onSampledReceived(self, data):
        pass

    def onIntervalReached(self):
        if not self.media_played:
            #swtich ui from time
            if 3 >= self.current_session_seconds >= 1 :
                self.newSessionIndicateUi()
                self.inform_text.setText('{} s until start, standby...'.format(3 - self.current_session_seconds))
            #cue
            elif self.current_session_seconds == 4:
                self.clearUi()
                self.cueImageUi()
            #action observation video
            elif self.current_session_seconds == 6:
                self.clearUi()
                self.actionObserveUi()
            
            # cue 
            elif self.current_session_seconds == 12:
                self.clearUi()
                self.cueImageUi()
            
            #start 1s early and 1s late to deal with data latency
            elif self.current_session_seconds == 13:
                #start thread
                pass
            #recordd for 6s
            elif self.current_session_seconds == 14:
                self.clearUi()

            elif self.current_session_seconds == 21:
                #restart session
                # self.current_session_seconds = 1
                
                #stop everythoing
                self.timer.stop()
                
            else:
                self.current_session_seconds += 1
            
        else:
            pass

    def onMediaStateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            print('playing...')
            self.media_played = True
        else:
            print('done')
            self.current_session_seconds = 12
            self.media_played = False


    def onStartBtnClicked(self):
        if self.sw == 0:
            print('Start')
            self.clearUi()
            self.startUi
        if self.sw == 1:
            print('Cue UI')
            self.clearUi()
            self.cueImageUi()
        if self.sw == 2:
            print('Video UI')
            self.clearUi
            self.actionObserveUi()
            
        self.sw  = (self.sw + 1) % 3

    # Auxillaries------------------------------------------------------
    def export(self):
        pass
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
    apply_stylesheet(app, theme = 'dark_cyan.xml')
    m = mainWindow()
    # m.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    # m.resize(800,600)
    # m.showMaximized()
    m.show()
    sys.exit(app.exec_())    