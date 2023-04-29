import sys, os
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from gtts import gTTS
from create_dataset import capture
from train_model import train_model
from detect import detection

# Set file path locations
model_file = 'Trained_model.h5'
tr_path = ".\\signs\\training\\"
v_path = ".\\signs\\validation\\"
te_path = ".\\signs\\test\\"

train_status = False

# GUI for create_database 
class GestureAdd(QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Add")
        self.setGeometry(300, 300, 400, 230)
        self.setStyleSheet("QWidget {background-color: rgb(56, 56, 56);}")
        
        _file = open(".\\signs\\counter.txt", "r+")
        self.ges_counter = int(_file.read())
        _file.close()
        
        self.title_label = QLabel("Gesture Add", self)
        self.title_label.move(115, 0)
        self.title_label.setStyleSheet(
                                "QLabel {color: red; font-weight: bold;}")
        self.title_label.adjustSize()
        
        self.label = QLabel("Enter gesture name: ", self)
        self.label.move(125, 40)
        self.label.setFont(QFont('Arial', 12))
        self.label.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label.adjustSize()
        
        self.label2 = QLabel(f"Gestures added: {self.ges_counter}", self)
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

        self.enter = QPushButton("Enter", self)
        self.enter.setGeometry(60, 170, 130, 50)
        self.enter.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.back = QPushButton("Exit", self)
        self.back.setGeometry(220, 170, 130, 50)
        self.back.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.enter.clicked.connect(self.addGesture)
        self.back.clicked.connect(self._exit)
        
        
    def addGesture(self):
        if self.textbox.text() != '':
            counter = capture(tr_path + self.textbox.text(),
                           v_path + self.textbox.text())
            self.ges_counter = self.ges_counter + counter
            self.label2.setText(f"Gestures added: {self.ges_counter}")
            _file = open(".\\signs\\counter.txt", "w")
            _file.write(str(self.ges_counter))
            _file.close()
        else:
            print("The text box is empty")
    
    def _exit(self, event):
        self.close()
        self.closed.emit()
         
    def closeEvent(self, event):
        self.closed.emit()
        
# GUI for train_model
class TrainModel(QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train Model")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("QWidget {background-color: rgb(56, 56, 56);}")
        
        self.title_label = QLabel("Training the model", self)
        self.title_label.move(280, 0)
        self.title_label.setStyleSheet(
                    "QLabel {color: red; font-weight: bold;}")
        self.title_label.adjustSize()
        
        self.label = QLabel("The program will process the training &" + 
        " validation data that trains the AI, it then stores the results\nof"+
        " the training into a file. Training status will update once" +
        " complete.", self)
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
        self.start.setGeometry(100, 500, 300, 50)
        self.start.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.back = QPushButton("Exit", self)
        self.back.setGeometry(420, 500, 300, 50)
        self.back.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.start.clicked.connect(self.startTraining)
        self.back.clicked.connect(self._exit)
        
        
    def startTraining(self):
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
        " validation data that trains the AI, it then stores the results" +
        " of the training into a file." +
        " Training status will update once complete.")
        
        self.title_label.move(510, 0)
        self.label.move(20, 50)
        self.label2.move(20, 120)
        self.label3.move(570, 700)
        self.start.move(400, 730)
        self.label_png.move(0, 200)
        self.label2_png.move(650, 200)
        
    def _exit(self, event):
        self.close()
        self.closed.emit()
        
    def closeEvent(self, event):
        self.closed.emit()

# GUI for detect
class Recognise(QWidget):
    closed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recognise")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("QWidget {background-color: rgb(56, 56, 56);}")
        
        # Creating and resetting the phrase text file.
        _file = open('.\\signs\\phrase.txt', 'w+')
        _file.write('')
        _file.close()
        self.path = os.getcwd() + '\\mpg123\\'
        
        self.title_label = QLabel("Recognising your hand gestures", self)
        self.title_label.move(180, 0)
        self.title_label.setStyleSheet(
            "QLabel {color: red; font-weight: bold;}")
        self.title_label.adjustSize()
        
        self.label = QLabel("The program will write out the user's gestures" +
        " into a string:\n Press C once started to capture a gesture.\n" +
        " Press V to exit the recogntion program.\n Press S to add space.\n" +
        " After exiting it will "
        " then show the phrase within this GUI.", self)
        self.label.move(20, 50)
        self.label.setFont(QFont('Arial', 12))
        self.label.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label.adjustSize()
        
        self.label2 = QLabel("Phrase will appear here", self)
        self.label2.move(240, 300)
        self.label2.setFont(QFont('Arial', 20))
        self.label2.setStyleSheet("QLabel {color: cyan; font-weight: bold;}")
        self.label2.adjustSize()
        
        self.start = QPushButton("Start Recognise", self)
        self.start.setGeometry(20, 500, 245, 50)
        self.start.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")

        self.read_out = QPushButton("Read Out", self)
        self.read_out.setGeometry(273, 500, 250, 50)
        self.read_out.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.back = QPushButton("Exit", self)
        self.back.setGeometry(530, 500, 245, 50)
        self.back.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
        self.start.clicked.connect(self.recognition)
        self.read_out.clicked.connect(self.readOut)
        self.back.clicked.connect(self._exit)
        
        
    def recognition(self):
        detection(te_path + 'hand.jpg', model_file)
        _file = open('.\\signs\\phrase.txt', 'r')
        phrase = _file.read()
        _file.close()
        
        self.label2.setText(phrase)
        self.label2.move(300, 300)
        print(phrase)
        
    def readOut(self):
        lang = 'en'
        myobj = gTTS(text = self.label2.text(), lang = lang, slow=False)
        os.chdir(self.path)
        myobj.save("phrase.mp3")
        os.system("mpg123 phrase.mp3")
        
    def _exit(self, event):
        self.close()
        self.closed.emit()
        
    def closeEvent(self, event):
        self.closed.emit()


# Main Menu GUI
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
        
        title_label = QLabel("Sign Language Recogniser", self)
        title_label.move(240, 0)
        title_label.setStyleSheet("QLabel {color: red; font-weight: bold;}")
        title_label.adjustSize()
        
        ges_label = QLabel("Add hand gesture to the program's dataset", self)
        ges_label.move(270, 135)
        ges_label.setFont(QFont('Arial', 18))
        ges_label.setStyleSheet(
        "QLabel {color: white; font-style: italic; border: 1px solid black;}")
        ges_label.adjustSize()
        
        tr_label = QLabel("Train the program's AI to the dataset", self)
        tr_label.move(270, 285)
        tr_label.setFont(QFont('Arial', 18))
        tr_label.setStyleSheet(
        "QLabel {color: white; font-style: italic; border: 1px solid black;}}")
        tr_label.adjustSize()
        
        rec_label = QLabel(
            "Have the program's AI recognise hand gestures", self)
        rec_label.move(270, 435)
        rec_label.setFont(QFont('Arial', 18))
        rec_label.setStyleSheet(
        "QLabel {color: white; font-style: italic; border: 1px solid black;}}")
        rec_label.adjustSize()
        
        ges_button = QPushButton("Add Gesture", self)
        tr_button = QPushButton("Train", self)
        rec_button = QPushButton("Recognise", self)
        
        ges_button.setGeometry(50, 125, 200, 50)
        ges_button.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        tr_button.setGeometry(50, 275, 200, 50)
        tr_button.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        rec_button.setGeometry(50, 425, 200, 50)
        rec_button.setStyleSheet(
            "QPushButton {background-color: rgb(66, 66, 66); color: cyan;}")
        
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
        
    # text-decoration: underline - For underlining text
        

app = QApplication(sys.argv)
window = Menu()
window.show()
_file = open(".\\signs\\counter.txt", "w+")
_file.write("0")
_file.close()
sys.exit(app.exec())