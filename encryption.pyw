from math import trunc
from optparse import check_choice
from this import d
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6 import QtGui


import sys
from striprtf.striprtf import rtf_to_text
import mimetypes


global file_url
file_url = None

# Setting up application
app = QApplication(sys.argv)


accepted_types = [
    'text/html', 
    'text/plain', 
    'application/rtf',
    'application/xml', 
    'application/cfg',
    'application/javascript',
    'application/python',
    'text/x-python',
    'application/vbs'

]

type = None

def check_file_ext(ext):

    global type
    # File checker (if not recognizing)
    if ext[-3:] == "cfg":
        type  = 'application/cfg'

    if ext[-3:] == "pyw":
        type = 'application/python'

    if ext[-2:] == "py":
        type = 'application/python'

    if ext[-3:] == "vbs":
        type = 'application/vbs'

#Actual reading file


times = 0

def read_file(url):
    
    global file_url 
    file_url = url

    global type
    global times

    #Guessing file type
    type = mimetypes.guess_type(url)
    type = type[0]

    if type == None:
        check_file_ext(url)

    #If still cannot read file type, ensure to say right thing
    if type == None:
        return (f"No current support for .{url.split('.')[-1]} files.")
    
    if type not in accepted_types:
        return f"No current support for {type} files."


    with open(url, 'r') as file:
        
        text= file.read()

    if url[-3:] == 'rtf':
        # If Mac Rich text File, do some weird stripping
        text = rtf_to_text(text)


    if times==0:
        times = 1
        return read_file(url)
    elif times == 1:
        times = 0
        return text





# When file dialog called

def b_pressed(self):
    x = QFileDialog.getOpenFileName(window, "Open file", "~/", 'All files (*)')

    if x[0] != "": #if there is actually a file selected and not cancelled

        text = read_file(x[0])
        window.label.setText(text)
        window.adjustSize()
        window.label.adjustSize()
        window.label.setText(text)
        
        window.adjustSize()
        window.label.adjustSize()



#Menu buttons
def encrypt_pressed(self):
    window.container.show()
    window.setCentralWidget(window.container)

def decrypt_pressed(self):
    print("decrypt")

    

def actual_encrypt_button_pressed(self):

    encrypt_key = window.encrypt_key_input.text()
    if file_url == None or (encrypt_key == "" or encrypt_key == "Key is required"):
        
        if encrypt_key == "":
            window.encrypt_key_input.setText("Key is required")
        
        if file_url == None:
            window.label.setText("Click to browse or drag files here (Required)")
            

    else: #if encryption is allowed to happen
        print(file_url)
        print(encrypt_key)

        

# Setting up windows
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True) # Accepting drag drops




        self.setWindowTitle("File Encryptor")

        self.label = QLabel("Click to browse or drag files here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.mousePressEvent = b_pressed
        self.label.setFont(QFont('.AppleSystemUIFont', 20))
        self.label.setMaximumHeight(120)


        button_layout = QHBoxLayout()
        self.encrypt_label = QLabel("Enter encryption key:")
        self.encrypt_key_input = QLineEdit()
        self.encrypt_key_input.setToolTip("Give this key to the other person")
        self.encrypt_key_input.setMinimumWidth(90)
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(actual_encrypt_button_pressed)

        button_layout.addWidget(self.encrypt_label)
        button_layout.addWidget(self.encrypt_key_input)
        button_layout.addWidget(self.encrypt_button)
        


        # Drag and Drop widget


        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)


        self.container = QWidget()
        self.container.setLayout(layout)
        self.container.hide()


        # Main Menu

        menu_layout = QVBoxLayout()

        self.menu_encrypt = QPushButton("Encrypt")
        self.menu_encrypt.clicked.connect(encrypt_pressed)

        self.menu_decrypt = QPushButton("Decrypt")
        self.menu_decrypt.clicked.connect(decrypt_pressed)

        menu_layout.addWidget(self.menu_encrypt)
        menu_layout.addWidget(self.menu_decrypt)

        self.menu_container = QWidget()
        self.menu_container.setLayout(menu_layout)

        self.setCentralWidget(self.menu_container)

        

    # Drag and Drop functioning


    

    
    def dragEnterEvent(self, event):

        self.temp_text = self.label.text()

        app.setStyleSheet("QMainWindow { background-color: grey }")


        if event.mimeData().hasUrls():
            self.label.setText("Release to read file!")
            event.accept()
            print("event")
        else:
            self.label.setText("Double check what you're dropping.")
            event.ignore()


    def dragLeaveEvent(self, event):

        app.setStyleSheet("")
        self.label.setText(self.temp_text)



    def dropEvent(self, event):
        app.setStyleSheet("")

        url = event.mimeData().urls()[0].toLocalFile()
            

        
        text = read_file(url)
        self.label.setText(text)
        self.adjustSize()
        self.label.adjustSize()
        self.label.setText(text)
        
        self.adjustSize()
        self.label.adjustSize()
        


        

        


window = MainWindow()

window.show()

# App exec loop
app.exec()