import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import requests
import json

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle("GUI")
        self.setStyleSheet("background-color: grey;")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.move(50, 80)
        
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setStyleSheet("background-color: yellow; border: 4px solid black;")
        self.label2.move(60, 100)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.move(60, 60)
        self.b1.setStyleSheet("background-color: yellow; border: 2px solid black;")
        self.b1.setText("Show BlockChain")
        self.b1.clicked.connect(self.clicked)
        
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.move(200, 60)
        self.b2.setStyleSheet("background-color: blue; border: 2px solid black;")
        self.b2.setText("Start Mining")
        self.b2.clicked.connect(self.clicked2)
        
        self.b3 = QtWidgets.QPushButton(self)
        self.b3.move(350, 60)
        self.b3.setStyleSheet("background-color: green; border: 2px solid black;")
        self.b3.setText("New Transaction")
        self.b3.clicked.connect(self.clicked3)

    def clicked(self):
        r = requests.get("http://0.0.0.0:6969/chain")
        self.label2.setText(json.dumps(r.json(), indent=2, sort_keys=True))
        self.update()

    def clicked2(self):
        r = requests.get("http://0.0.0.0:6969/mine")
        self.label2.setText(json.dumps(r.json(), indent=2, sort_keys=True))
        self.update()
    
    def clicked3(self):
        r = requests.post("http://0.0.0.0:6969/transaction/new", data={'sender': 'tester','recipient': '1234','amount': 6}, headers={'Content-Type':'application/json'})
        if r.status_code == 201:
            self.label2.setText(json.dumps(r.json(), indent=2, sort_keys=True))
            self.update()


    def update(self):
        self.label2.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()





