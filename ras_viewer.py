#!/usr/bin/env python3

import sys
import datetime
import csv

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPen

from collections import defaultdict
from items import Items
from dag_graphs import WaterPlants, WalkDog, TakeMedication
from detect_error import check_sequence

class RAS(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates application UI'''

        self.board = Board(self)
        self.setCentralWidget(self.board)

        self.statusbar = self.statusBar()
        self.board.msg2Statusbar[str].connect(self.statusbar.showMessage)
        self.board.start()

        self.resize(820, 435)
        self.center()
        self.setWindowTitle('RAS')
        self.show()

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
            (screen.height()-size.height())/2)

class Board(QFrame):

    msg2Statusbar = pyqtSignal(str)

    BoardWidth = 595
    BoardHeight = 380
    Speed = 250
    FastSpeed = 50
    Dag = {'water_plants': WaterPlants,
           'walk_dog': WalkDog,
           'take_meds': TakeMedication}

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        self.sequence = defaultdict(list)
        with open('estimotes_full_labeled.data', newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.startDatetime = None
            for row in data:
                dt = datetime.datetime.strptime(row[0] + ' ' + row[1], "%Y-%m-%d %H:%M:%S")
                if self.startDatetime is None:
                    self.startDatetime = dt
                time_diff = (dt - self.startDatetime).total_seconds()
                status = True if row[3] == 'start' else False
                if len(row) > 4:
                    self.sequence[int(time_diff)].append((row[2], status, row[4], True if row[5] == 'start' else False))
                else:
                    self.sequence[int(time_diff)].append((row[2], status))

        self.outputFile = open('error_prediction.txt', 'w')
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.timeCounter = -1
        self.taskName = ""
        self.taskStatus = False
        self.taskSequence = []
        self.clearBoard()

        self.sensor = Sensor()
        label = QLabel('umbrella', self)
        label.move((20*30)+10+10+17, 13)
        label = QLabel('leash', self)
        label.move((20*30)+10+10+17, 13+20)
        label = QLabel('keys', self)
        label.move((20*30)+10+10+17, 13+40)
        label = QLabel('dog', self)
        label.move((20*30)+10+10+17, 13+60)
        label = QLabel('snack', self)
        label.move((20*30)+10+10+17, 13+80)
        label = QLabel('cup', self)
        label.move((20*30)+10+10+17, 13+100)
        label = QLabel('medication bottle', self)
        label.move((20*30)+10+10+17, 13+120)
        label = QLabel('watering can', self)
        label.move((20*30)+10+10+17, 13+140)

        self.textboxSequence = QLineEdit(self)
        self.textboxSequence.move(0, 380)
        self.textboxSequence.resize(Board.BoardWidth, 30)

        self.textboxDetectError = QLineEdit(self)
        self.textboxDetectError.move(Board.BoardWidth, 380)
        self.textboxDetectError.resize(820-Board.BoardWidth, 30)


    def start(self):
        '''starts simulation'''

        if self.isPaused:
            return

        self.isStarted = True
        self.sequenceCounter = 0
        self.clearBoard()

        self.timeCounter = -1
        self.msg2Statusbar.emit('total seconds: '+ str(self.timeCounter+1))

        self.timer.start(Board.Speed, self)

    def paintEvent(self, event):
        '''paints all estimote triggered sensors'''

        painter = QPainter(self)
        rect = self.contentsRect()
        pixmap = QPixmap('layout.jpg')
        painter.drawPixmap(QRect(0, 0, pixmap.width(), pixmap.height()), pixmap)

        for sensor_name in self.sensor.values:
            self.drawSensor(
                painter,
                position=self.sensor.values[sensor_name]['position'],
                size=self.sensor.values[sensor_name]['size'],
                color=self.sensor.values[sensor_name]['color'],
                isOn=self.sensor.values[sensor_name]['ON'])

    def drawSensor(self, painter, position=(0, 0), size=(0, 0), color=0x00FF00, isOn=False):
        ''' draw sensor in simulation'''

        x, y = position
        w, h = size
        if isOn:
            painter.setBrush(QColor(color))
            #painter.setPen(QPen(QColor(0x55, 0x55, 0xFF),2))
            painter.drawEllipse(x+1, y+1, w, h)

        #painter.fillRect(x+1, y+1, w, h, color)
        #painter.setPen(QColor(0x0000FF))
        #painter.drawRect(x+1, y+1, w, h)

    def pause(self):
        '''pauses simulation'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")
        else:
            self.timer.start(Board.Speed, self)
            currentTime = self.startDatetime + datetime.timedelta(0, self.timeCounter)
            currentTimeStr = currentTime.strftime("%Y-%m-%d %H:%M:%S")
            self.msg2Statusbar.emit('Simulation Time: {}'.format(currentTimeStr))

        self.update()

    def restart(self):
        '''restart simulation'''

        if not self.isStarted:
            return

        self.timeCounter = -1
        self.sequenceCounter = 0
        currentTimeStr = self.startDatetime.strftime("%Y-%m-%d %H:%M:%S")
        self.msg2Statusbar.emit('Simulation Time: {}'.format(currentTimeStr))
        #self.update()

    def stop(self):
        self.restart()
        self.pause()
        self.outputFile.close()

    def keyPressEvent(self, event):
        '''processes key press events'''

        if not self.isStarted:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return
        elif key == Qt.Key_R:
            self.restart()
            return
        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        '''handles timer event'''

        if event.timerId() == self.timer.timerId():
            self.timeCounter += 1

            if self.timeCounter in self.sequence:
                self.sequenceCounter += 1

            if self.sequenceCounter > len(self.sequence):
                self.stop()
                return

            isStopTask = False
            for seq in self.sequence[self.timeCounter]:
                self.sensor.values[seq[0]]['ON'] = seq[1]
                seq_code = Items.encode[seq[0][:-2]][1]
                if len(seq) > 2:
                    self.taskName = seq[2]
                    if seq[3]:
                        self.taskStatus = True
                        self.textboxSequence.setText("")
                        self.textboxDetectError.setText("")
                        self.taskSequence = []
                        self.timer.stop()
                        self.timer.start(Board.Speed, self)
                    else:
                        isStopTask = True
                        self.taskStatus = False
                        self.timer.stop()
                        self.timer.start(Board.FastSpeed, self)

                if isStopTask or (seq[1] and self.taskStatus):
                    if seq[1]: self.taskSequence.append(seq_code)
                    errorStatus = check_sequence(
                        Board.Dag[self.taskName].taskStart,
                        seq=self.taskSequence,
                        task_num=Board.Dag[self.taskName].numTasks)

                    if self.textboxSequence.text() == "":
                        self.textboxSequence.setText(seq_code)
                    else:
                        self.textboxSequence.setText(self.textboxSequence.text() + "-" + seq_code)

                    # Simulation in progress
                    if self.taskStatus:
                        subtaskName =  errorStatus[2]
                        if errorStatus[1]:
                            self.textboxDetectError.setStyleSheet("background-color:#00ff00;")
                        else:
                            self.textboxDetectError.setStyleSheet("background-color:#ff0000;")
                        self.textboxDetectError.setText(subtaskName)

                    # Task has ended
                    elif isStopTask:
                        isStopTask = False
                        self.outputFile.write("{}: {}\n".format(self.taskName, self.textboxSequence.text()))
                        self.outputFile.write("prediction: {}\n\n".format(errorStatus))
                        subtaskName =  errorStatus[4]
                        if errorStatus[3]:
                            subtaskName = self.taskName + ": " + subtaskName
                            self.textboxDetectError.setStyleSheet("background-color:#00ff00;")
                        else:
                            self.textboxDetectError.setStyleSheet("background-color:#ff0000;")
                    self.textboxDetectError.setText(subtaskName)

            currentTime = self.startDatetime + datetime.timedelta(0, self.timeCounter)
            currentTimeStr = currentTime.strftime("%Y-%m-%d %H:%M:%S")
            if self.taskStatus:
                self.msg2Statusbar.emit('Simulation Time: {}   Task: {}'.format(currentTimeStr, self.taskName))
            else:
                self.msg2Statusbar.emit('Simulation Time: {}'.format(currentTimeStr))
            self.update()
        else:
            super(Board, self).timerEvent(event)

    def clearBoard(self):
        '''clears board'''
        pass


class Sensor(object):

    COLOR_1 = 0x00FF00
    COLOR_2 = 0x0000FF

    def __init__(self):

        self.values = {'sink_tap_1':
                          {'ON': False,
                           'position': ((20*22)-8, 15), # x,y
                           'size': (20, 20), # w,h
                           'color': self.COLOR_1},
                       'sink_tap_2':
                          {'ON': False,
                           'position': ((20*22)-8+20, 15),
                           'size': (20, 20),
                           'color': self.COLOR_2},
                       'garbage_1':
                          {'ON': False,
                           'position': ((20*21)+2, 45),
                           'size': (15, 15),
                           'color': self.COLOR_1},
                       'garbage_2':
                          {'ON': False,
                           'position': ((20*21)+2+15, 45),
                           'size': (15, 15),
                           'color': self.COLOR_2},
                       'chair_1':
                          {'ON': False,
                           'position': ((20*7)+2, 65),
                           'size': (20, 20),
                           'color': self.COLOR_1},
                       'chair_2':
                          {'ON': False,
                           'position': ((20*7)+2+20, 65),
                           'size': (20, 20),
                           'color': self.COLOR_2},
                       'windowsill_plant_1':
                          {'ON': False,
                           'position': ((20*29)-3, 87),
                           'size': (20, 20),
                           'color': self.COLOR_1},
                       'windowsill_plant_2':
                          {'ON': False,
                           'position': ((20*29)-3, 87+20),
                           'size': (20, 20),
                           'color': self.COLOR_2},
                       'coffee_table_plant_1':
                          {'ON': False,
                           'position': ((20*6)-1, 240),
                           'size': (28, 28),
                           'color': self.COLOR_1},
                       'coffee_table_plant_2':
                          {'ON': False,
                           'position': ((20*6)-1+28, 240),
                           'size': (28, 28),
                           'color': self.COLOR_2},
                       'side_table_plant_1':
                          {'ON': False,
                           'position': (24, 175),
                           'size': (28, 28),
                           'color': self.COLOR_1},
                       'side_table_plant_2':
                          {'ON': False,
                           'position': (24+28, 175),
                           'size': (28, 28),
                           'color': self.COLOR_2},
                       'door_1':
                          {'ON': False,
                           'position': ((20*29)-3, 265),
                           'size': (20, 20),
                           'color': self.COLOR_1},
                       'door_2':
                          {'ON': False,
                           'position': ((20*29)-3, 265+20),
                           'size': (20, 20),
                           'color': self.COLOR_2},
                       'umbrella_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'umbrella_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15),
                           'size': (10, 10),
                           'color': self.COLOR_2},
                       'leash_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15+20),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'leash_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15+20),
                           'size': (10, 10),
                           'color': self.COLOR_2},
                       'keys_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15+40),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'keys_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15+40),
                           'size': (10, 10),
                           'color': self.COLOR_2},
                       'dog_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15+60),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'dog_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15+60),
                           'size': (10, 10),
                           'color': self.COLOR_2},
                       'food_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15+80),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'food_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15+80),
                           'size': (10, 10),
                           'color': self.COLOR_2},
                       'cup_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15+100),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'cup_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15+100),
                           'size': (10, 10),
                           'color': self.COLOR_2},
                       'medication_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15+120),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'medication_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15+120),
                           'size': (10, 10),
                           'color': self.COLOR_2},
                       'water_can_1':
                          {'ON': False,
                           'position': ((20*30)+10, 15+140),
                           'size': (10, 10),
                           'color': self.COLOR_1},
                       'water_can_2':
                          {'ON': False,
                           'position': ((20*30)+10+10, 15+140),
                           'size': (10, 10),
                           'color': self.COLOR_2}}



if __name__ == '__main__':

    app = QApplication([])
    ras = RAS()
    sys.exit(app.exec_())
