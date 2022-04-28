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
import pickle

from pylsl import StreamInlet, resolve_stream

# ref https://stackoverflow.com/questions/47339044/pyqt5-timer-in-a-thread
class DataCaptureThread(QThread):
    def __init__(self):
        super(DataCaptureThread, self).__init__()
        self.sampling_timer = QTimer()
        self.cnt = 0
        # Init lsllib
        self.is_intialized = False
        self.eeg_data = []

        
        print('Start intialize the eeg stream')
        streams = resolve_stream('type', 'EEG')

        self.inlet = StreamInlet(streams[0])
        self.is_intialized = True
        
        self.sampling_timer.timeout.connect(self.collect)
        self.sampling_timer.moveToThread(self)
    def collect(self):
        sample, timestamp = self.inlet.pull_sample()
        self.eeg_data.append((timestamp, sample))
            # t = datetime.datetime.now()
            # print("THREAD-Collecting data at {}:{}:{}".format(t.hour, t.minute, t.second))

    def run(self):
        self.sampling_timer.start(2)
        loop = QEventLoop()
        loop.exec_()
    
    def stop_timer(self):
        self.sampling_timer.stop()
    
    def export(self, fname):
        with open(fname, 'w') as f:
            for l in self.eeg_data:
                ts = str(l[0])
                d = ' '.join([str(i) for i in l[1]])
                f.writelines(ts + ' ' + d + '\n')
        # print(self.eeg_data[:1])

class baseWindow(QMainWindow):
    def __init__(self, parent = None):
        super(baseWindow, self).__init__()
        self.setWindowTitle('Test Test')


        self.sc = QWidget()
        self.sc.setStyleSheet("background-color: black")
        self.setCentralWidget(self.sc)
        #Add Horizontal layout
        self.baseContainer = QVBoxLayout()
        self.baseContainer.setContentsMargins(0,0,0,0)
        
        # Content 
        self.start_btn = QPushButton('Start Recording Sequece')
        self.start_btn.setEnabled(True)
        # self.start_btn.setStyleSheet('color: white}')
        self.start_btn.setProperty('class', 'danger')
        self.start_btn.resize(150, 50)
        self.start_btn.clicked.connect(self.onStartBtnClicked) 

        self.cue_img = QLabel('dummy')
        self.cue_img.setStyleSheet('color: white;')
        self.cue_img.setAlignment(Qt.AlignCenter)

        self.action_obersve_video = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.action_obersve_video)
        self.media_player.setMedia(QMediaContent(QUrl('cat.mp4')))
        self.media_player.stateChanged.connect(self.mediaStateChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.positionChanged.connect(self.positionChanged)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0,0)
        self.position_slider.sliderMoved.connect(self.setPosition)

        # self.baseContainer.addWidget(self.action_obersve_video)
        self.baseContainer.addStretch()
        self.baseContainer.addWidget(self.cue_img)
        # self.baseContainer.addWidget(self.position_slider)
        # baseContainer.addWidget(self.vidBtnSpacer)
        self.baseContainer.addStretch()
        self.baseContainer.addWidget(self.start_btn)
        self.sc.setLayout(self.baseContainer)

        #thread
        self.collect_thread = DataCaptureThread()
    
        #timer for adpative display
        self.current_time = 0
        self.interval_timer = QTimer()
        self.interval_timer.timeout.connect(self.shiftDisplay)

        self.is_done_playing = False

    def shiftDisplay(self):
        t = datetime.datetime.now()
        # print("TEST-Collecting data at {}:{}:{}:{}".format(t.hour, t.minute, t.second, t.microsecond * 1000))
        # self.collect_thread.cnt = 0
        print(self.is_done_playing)
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
            self.media_player.play()
        
        if self.is_done_playing:

            self.cue_img = QLabel('dummy')
            self.cue_img.setStyleSheet('color: white;')
            self.cue_img.setAlignment(Qt.AlignCenter)

            print(self.baseContainer.count())
            item = self.baseContainer.itemAt(1) #video
            widget = item.widget()
            widget.deleteLater()
            #Insert AO
            self.baseContainer.insertWidget(1,self.cue_img)
            self.cue_img.setText('Ready')
            self.is_done_playing = False
            self.interval_timer.stop()
            self.current_time = 0 
            print(len(self.collect_thread.eeg_data))
            self.collect_thread.export()
        
        self.current_time += 1

    
    def clearLayout(self):
        pass
        

    def recordStart(self):
        self.baseContainer.addStretch()
        self.baseContainer.addWidget(self.cue_img)
        self.baseContainer.addStretch()
        self.baseContainer.addWidget(self.start_btn)
        self.sc.setLayout(self.baseContainer)
        
            
    def onStartBtnClicked(self):
        print(self.baseContainer.count())
        self.interval_timer.start(1000)
        self.collect_thread.start()
        
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
            print('pause')
            self.collect_thread.stop_timer()
            self.collect_thread.terminate()
            self.is_done_playing = True

    def setPosition(self, position):
        self.media_player.setPosition(position)
    
    def positionChanged(self, position):
        self.position_slider.setValue(position)
        # print('set slider postion :', position)
    
    def durationChanged(self, duration):
        self.position_slider.setRange(0, duration)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
    apply_stylesheet(app, theme = 'dark_cyan.xml')
    m = baseWindow()
    m.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    # m.resize(800,600)
    m.showMaximized()
    m.show()
    sys.exit(app.exec_())      
        