import sys, random
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from pathlib import Path
from create_dataset import webcam
from train_model import train_model
from detect import detection

global model_file, tr_path, v_path, te_path

model_file = 'Trained_model_backup.h5'
        
# Path Checking + Creating folders
        
tr_path = ".\\signs\\training\\"
v_path = ".\\signs\\validation\\"
te_path = ".\\signs\\test\\"
'''
paths = [tr_path, v_path, te_path]
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)
'''
    
print("Welcome to the developer version of SLR program :0")

class GestureAdd(QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Add")
        self.setGeometry(300, 300, 400, 200)
        self.setStyleSheet("QWidget {background-color: rgb(56, 56, 56);}")
        
        self.title_label = QLabel("Gesture Add", self)
        self.title_label.move(115, 0)
        self.title_label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        self.title_label.adjustSize()
        
        self.label = QLabel("Enter gesture name: ", self)
        self.label.move(125, 40)
        self.label.setFont(QFont('Arial', 12))
        self.label.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label.adjustSize()
        
        self.label2 = QLabel("Once done, press the exit button ", self)
        self.label2.move(80, 120)
        self.label2.setFont(QFont('Arial', 12))
        self.label2.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label2.adjustSize()
        
        self.textbox = QLineEdit(self)
        self.textbox.move(60, 70)
        self.textbox.resize(280,40)
        self.textbox.setStyleSheet("QLineEdit {color: white;}")


        self.back = QPushButton("Enter", self)
        self.back.setGeometry(100, 145, 200, 50)
        self.back.setStyleSheet("QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")

        
        self.back.clicked.connect(self.pressed)
        
    def pressed(self):
        # Creates folders for the newly added gestures
        paths = [tr_path + self.textbox.text(), v_path + self.textbox.text()]
        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=True)
        webcam(paths[0], paths[1])
        
         
    def closeEvent(self, event):
        self.closed.emit()


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None
        
        self.setWindowTitle("MainWindow")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("QMainWindow {background-color: rgb(56, 56, 56);}")
        QApplication.setFont(QFont('Arial', 20), "QLabel")
        QApplication.setFont(QFont('Arial', 20), "QLineEdit")
        
        self.UIComponents()

    def UIComponents(self):
        
        # text-decoration: underline
        
        title_label = QLabel("Sign Language Recogniser", self)
        title_label.move(240, 0)
        title_label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        title_label.adjustSize()
        
        ges_label = QLabel("Add hand gesture to the program's dataset", self)
        ges_label.move(270, 135)
        ges_label.setFont(QFont('Arial', 18))
        ges_label.setStyleSheet("QLabel {color: white; font-style: italic; border: 1px solid black;}")
        ges_label.adjustSize()
        
        tr_label = QLabel("Train the program's AI to the dataset", self)
        tr_label.move(270, 285)
        tr_label.setFont(QFont('Arial', 18))
        tr_label.setStyleSheet("QLabel {color: white; font-style: italic; border: 1px solid black;}}")
        tr_label.adjustSize()
        
        rec_label = QLabel("Have the program's AI recognise hand gestures", self)
        rec_label.move(270, 435)
        rec_label.setFont(QFont('Arial', 18))
        rec_label.setStyleSheet("QLabel {color: white; font-style: italic; border: 1px solid black;}}")
        rec_label.adjustSize()
        
        
        ges_button = QPushButton("Add Gesture", self)
        tr_button = QPushButton("Train", self)
        rec_button = QPushButton("Recognise", self)
        
        ges_button.setGeometry(50, 125, 200, 50)
        ges_button.setStyleSheet("QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        tr_button.setGeometry(50, 275, 200, 50)
        tr_button.setStyleSheet("QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        rec_button.setGeometry(50, 425, 200, 50)
        rec_button.setStyleSheet("QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        
        ges_button.clicked.connect(self.gestureWindow)
        tr_button.clicked.connect(self.gestureWindow)
        rec_button.clicked.connect(self.gestureWindow)
        
    def gestureWindow(self):
        self.hide()
        if self.window is None:
            self.window = GestureAdd()
            print("hi")
        self.window.closed.connect(self.show)
        self.window.show()
        

app = QApplication(sys.argv)
window = Menu()
window.show()
sys.exit(app.exec())

'''
ges_button.clicked.connect(ges_button.deleteLater)
        ges_button.clicked.connect(tr_button.deleteLater)
        ges_button.clicked.connect(rec_button.deleteLater)
        ges_button.clicked.connect(title_label.deleteLater)
        ges_button.clicked.connect(ges_label.deleteLater)
        ges_button.clicked.connect(tr_label.deleteLater)
        ges_button.clicked.connect(rec_label.deleteLater)
'''