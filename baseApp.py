from random import sample
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir, Qt, QUrl, QThread, QTimer, QEventLoop
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QHBoxLayout, QVBoxLayout,
                            QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QWidget, QAction)
from PyQt5.QtGui import QIcon

from qt_material import apply_stylesheet
import datetime

import sys
import os
import time

from pylsl import StreamInlet, resolve_stream

class baseWindow(QMainWindow):
    def __init__(self, parent = None):
        super(baseWindow, self).__init__()
        self.setWindowTitle('Test Test')

        # self.action_obersve_video = QVideoWidget()
        # self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # self.media_player.setVideoOutput(self.action_obersve_video)
        # self.media_player.setMedia(QMediaContent(QUrl('IMG_2659.MOV')))
        # self.media_player.stateChanged.connect(self.mediaStateChanged)

            # self.baseContainer.insertWidget(1,self.action_obersve_video)


        self.action_obersve_video = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.action_obersve_video)
        self.media_player.setMedia(QMediaContent(QUrl('assets/IMG_2659.MOV')))
        self.action_obersve_video.resize(800, 600)
        self.media_player.stateChanged.connect(self.mediaStateChanged)
        # self.applyPage(self.showAOPage)        


        #timer for adpative display
        self.current_time = 0
        self.interval_timer = QTimer()
        self.interval_timer.timeout.connect(self.shiftDisplay)
        self.is_done_playing = False
    

        # #Display start page
        self.applyPage(self.startPa)
        self.test = 2

    def applyPage(self, fn):
        print(fn)
        self.widget, self.layout = fn()
        self.widget.setLayout(self.layout)

    def startPage(self):
        # Content 
        start_btn = QPushButton('Start Recording')
        start_btn.setEnabled(True)
        # self.start_btn.setStyleSheet('color: white}')
        start_btn.setProperty('class', 'danger')
        start_btn.resize(150, 50)
        start_btn.clicked.connect(self.onStartBtnClicked) 

        cue_img = QLabel('Ready')
        cue_img.setStyleSheet('color: white;')
        cue_img.setAlignment(Qt.AlignCenter)
        
        sc = QWidget()
        sc.setStyleSheet("background-color: black")
        self.setCentralWidget(sc)
        #Add Horizontal layout
        container = QVBoxLayout()
        container.setContentsMargins(0,0,0,0)

        container.addStretch()
        container.addWidget(cue_img)
        container.addStretch()
        container.addWidget(start_btn)
        # sc.setLayout(self.container)
        return sc, container

    def cuePage(self):

        start_btn = QPushButton('Start Recording')
        start_btn.setEnabled(True)
        # self.start_btn.setStyleSheet('color: white}')
        start_btn.setProperty('class', 'danger')
        start_btn.resize(150, 50)
        start_btn.clicked.connect(self.onStartBtnClicked) 

        cue_img = QLabel()
        cue_img.setAlignment(Qt.AlignCenter)
        cue_img.setPixmap(QtGui.QPixmap('assets/cue2.png'))
        
        sc = QWidget()
        sc.setStyleSheet("background-color: black")
        self.setCentralWidget(sc)
        #Add Horizontal layout
        container = QVBoxLayout()
        container.setContentsMargins(0,0,0,0)
        container.addStretch()
        container.addStretch()
        container.addWidget(cue_img)
        container.addStretch()
        container.addWidget(start_btn)
        # sc.setLayout(self.container)
        return sc, container
    
    def showAOPage(self):
            #Insert AO

        start_btn = QPushButton('Start Recording')
        start_btn.setEnabled(True)
        # self.start_btn.setStyleSheet('color: white}')
        start_btn.setProperty('class', 'danger')
        start_btn.resize(150, 50)
        start_btn.clicked.connect(self.onStartBtnClicked) 

        sc = QWidget()
        sc.setStyleSheet("background-color: black")
        self.setCentralWidget(sc)
        #Add Horizontal layout
        container = QVBoxLayout()
        container.setContentsMargins(0,0,0,0)

        return sc, container

    def clearLayout(self):
        print(self.layout)
        for i in reversed(range(self.layout.count())):
            try:
                self.layout.itemAt(i).widget().deleteLater()
            except AttributeError as e:
                print('Attemp to delete strecht')

    def shiftDisplay(self):
        t = datetime.datetime.now()
        print("data at {}:{}:{}:{}".format(t.hour, t.minute, t.second, t.microsecond * 1000))
        # Before playing
        if not self.is_done_playing:
            if  self.current_time < 2:
                self.cue_img.setText('Ready')
            
            elif self.current_time < 4:
                #Set cue
                self.cue_img.setText('Cue')

            elif self.current_time == 4:
                #Show AO
                item = self.baseContainer.itemAt(1) #remove label
                widget = item.widget()
                widget.deleteLater()
                #Insert AO
                self.baseContainer.insertWidget(1,self.action_obersve_video)
                self.media_player.setMuted(True)
                self.media_player.play()
            
        #after playing
        if self.is_done_playing:
            if  self.current_time < 2:
                self.cue_img = QLabel('dummy')
                self.cue_img.setStyleSheet('color: white;')
                self.cue_img.setAlignment(Qt.AlignCenter)

                item = self.baseContainer.itemAt(1) #video
                widget = item.widget()
                widget.deleteLater()
                self.baseContainer.insertWidget(1,self.cue_img)
                self.cue_img.setText('Ready to perform')

            elif self.current_time == 2:
                #play beep and remove everything
                item = self.baseContainer.itemAt(1) #remove label
                widget = item.widget()
                widget.deleteLater()
            elif 4>= self.current_time >= 2:
                # polling for data
                print("polling")
                pass
            elif self.current_time > 4:
                print('Done')
                self.interval_timer.stop()
                #export data
                # self.export()
        self.current_time += 1
        

    def recordStart(self):
        self.baseContainer.addStretch()
        self.baseContainer.addWidget(self.cue_img)
        self.baseContainer.addStretch()
        self.baseContainer.addWidget(self.start_btn)
        self.sc.setLayout(self.baseContainer)
        
            
    def onStartBtnClicked(self):
        
        # print(self.layout.count())
        # self.clearLayout()
        # self.applyPage(self.cuePage)
        if self.test == 1:
            self.applyPage(self.cuePage)
        elif self.test == 0:
            self.applyPage(self.showAOPage)
            self.layout.insertWidget(1,self.action_obersve_video)
            self.media_player.setMuted(True)
            self.media_player.play()

        print(self.test)
        self.test = (self.test + 1) % 2
        # self.interval_timer.start(1000)
        # self.collect_thread.start()
        
        # if self.media_player.state() == QMediaPlayer.PlayingState:
            # self.media_player.pause()
            # self.collect_thread.stop_timer()
            # self.collect_thread.terminate()
            # self.interval_timer.stop()
        # els
            # self.media_player.play()
            # self.collect_thread.start()
            # self.interval_timer.start(1000)

    def mediaStateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            print('play')
        else:
            print('done')
            self.is_done_playing = True
            #reset current time
            self.current_time = 0



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
    apply_stylesheet(app, theme = 'dark_cyan.xml')
    m = baseWindow()
    # m.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    m.resize(800,600)
    # m.showMaximized()
    m.show()
    sys.exit(app.exec_())      
        