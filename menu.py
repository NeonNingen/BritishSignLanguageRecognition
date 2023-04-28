import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from pathlib import Path
from create_dataset import webcam
from train_model import train_model
from detect import detection

model_file = 'Trained_model_backup.h5'
tr_path = ".\\signs\\training\\"
v_path = ".\\signs\\validation\\"
te_path = ".\\signs\\test\\"

ges_counter = 0
train_status = False


print("Welcome to the developer version of SLR program :0")

class GestureAdd(QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Add")
        self.setGeometry(300, 300, 400, 230)
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
        
        self.label2 = QLabel(f"Gestures added: {ges_counter}", self)
        self.label2.move(125, 115)
        self.label2.setFont(QFont('Arial', 12))
        self.label2.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label2.adjustSize()
        
        self.label3 = QLabel("Once done, press the exit button ", self)
        self.label3.move(80, 145)
        self.label3.setFont(QFont('Arial', 12))
        self.label3.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label3.adjustSize()
        
        self.textbox = QLineEdit(self)
        self.textbox.move(60, 70)
        self.textbox.resize(280,40)
        self.textbox.setStyleSheet("QLineEdit {color: white;}")


        self.back = QPushButton("Enter", self)
        self.back.setGeometry(100, 170, 200, 50)
        self.back.setStyleSheet("QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.back.clicked.connect(self.pressed)
        
        
    def pressed(self):
        if self.textbox.text() != '':
            counter = webcam(tr_path + self.textbox.text(),
                           v_path + self.textbox.text())
            self.label2.setText(f"Gestures added: {ges_counter + counter}")
            train_status = False
        else:
            print("The text box is empty")
         
    def closeEvent(self, event):
        self.closed.emit()
        
class TrainModel(QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train Model")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("QWidget {background-color: rgb(56, 56, 56);}")
        
        self.title_label = QLabel("Training the model", self)
        self.title_label.move(280, 0)
        self.title_label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        self.title_label.adjustSize()
        
        self.label = QLabel("The program will process the training &" + 
        " validation data that trains the AI, it then stores the results\nof the" +
        " training into a file. Training status will update once complete.", self)
        self.label.move(20, 50)
        self.label.setFont(QFont('Arial', 12))
        self.label.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label.adjustSize()
        
        self.label2 = QLabel(f"Training Status: {train_status}", self)
        self.label2.move(20, 120)
        self.label2.setFont(QFont('Arial', 12))
        self.label2.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label2.adjustSize()
        
        self.label3 = QLabel("Press button to start training", self)
        self.label3.move(300, 470)
        self.label3.setFont(QFont('Arial', 12))
        self.label3.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label3.adjustSize()
        
        self.start = QPushButton("Start Training", self)
        self.start.setGeometry(160, 500, 500, 50)
        self.start.setStyleSheet("QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.start.clicked.connect(self.pressed)
        
        
    def pressed(self):
        self.label3.setText("Training Complete")
        train_status = train_model(tr_path, v_path, model_file)
        if train_status:
            self.label2.setText(f"Training Status: {train_status}")
            
        self.setGeometry(100, 100, 1280, 800)
        self.label_png = QLabel(self)
        self.pixmap = QPixmap('./signs/graphs/acc_plot.jpg')
        self.label_png.setPixmap(self.pixmap)
        self.label_png.resize(self.pixmap.width(), self.pixmap.height())
        self.label_png.show()
        
        self.label2_png = QLabel(self)
        self.pixmap = QPixmap('./signs/graphs/loss_plot.jpg')
        self.label2_png.setPixmap(self.pixmap)
        self.label2_png.resize(self.pixmap.width(), self.pixmap.height())
        self.label2_png.show()
        
        self.label.setText("The program will process the training &" + 
        " validation data that trains the AI, it then stores the results of the" +
        " training into a file. Training status will update once complete.")
        
        self.title_label.move(510, 0)
        self.label.move(20, 50)
        self.label2.move(20, 120)
        self.label3.move(570, 700)
        self.start.move(400, 730)
        self.label_png.move(0, 200)
        self.label2_png.move(650, 200)
        
        
    def closeEvent(self, event):
        self.closed.emit()

class Recognise(QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recognise")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("QWidget {background-color: rgb(56, 56, 56);}")
        
        self.start = QPushButton("Start Recognise", self)
        self.start.setGeometry(160, 500, 500, 50)
        self.start.setStyleSheet("QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.start.clicked.connect(self.pressed)
        
        
    def pressed(self):
        detection(te_path + 'hand.jpg', model_file)
        
        
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
        tr_button.clicked.connect(self.trainWindow)
        rec_button.clicked.connect(self.detectWindow)
        
    def gestureWindow(self):
        self.window = None
        self.hide()
        if self.window is None:
            self.window = GestureAdd()
        self.window.closed.connect(self.show)
        self.window.show()
        
    def trainWindow(self):
        self.window = None
        self.hide()
        if self.window is None:
            self.window = TrainModel()
        self.window.closed.connect(self.show)
        self.window.show()
        
    def detectWindow(self):
        self.window = None
        self.hide()
        if self.window is None:
            self.window = Recognise()
        self.window.closed.connect(self.show)
        self.window.show()
        

app = QApplication(sys.argv)
window = Menu()
window.show()
sys.exit(app.exec())