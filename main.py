import sys, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

class ThreadedEmail(QtCore.QRunnable):

    def __init__(self, path, login_email, login_password, receiver_email, delay, isAttachmentIncluded):
        super().__init__()
        self.path = path
        self.login_email = login_email
        self.login_password = login_password
        self.receiver_email = receiver_email
        self.delay = delay
        self.isAttachmentIncluded = isAttachmentIncluded

    def run(self):
        app = QtCore.QCoreApplication.instance()
        sleep(self.delay)
        self.sendEmail()
        app.quit()

    def sendEmail(self):
        subject = "Subject of Email"
        body = "Body of Email"
        sender_email = self.login_email
        receiver_email = self.receiver_email
        password = self.login_password

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))
        filename = self.path

        if self.isAttachmentIncluded:
            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            # Add attachment to message and convert message to string
            message.attach(part)

        text = message.as_string()
        port = 465  # For SSL
        server = smtplib.SMTP_SSL("smtp.gmail.com", port)
        server.login(sender_email, password)
        try:
            server.sendmail(sender_email, receiver_email, text)
        finally:
            server.quit()
            print("Server Closed!")


class UserInterface(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        # --> Initialize QSettings file "*.ini"
        settingsFile = 'settings.ini'
        if not os.path.exists(settingsFile):
            open(settingsFile, 'a').close()
        self.settings = QSettings(settingsFile, QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.loadSettings()
        
        self.initUI()
        self.isFileWatcherOn = False

    def initUI(self):

        self.choseFile_btn = QtGui.QPushButton('Chose File', self)
        self.choseFile_btn.clicked.connect(self.fileOpen)
        self.choseFile_txtLine = QtGui.QLineEdit()
        
        self.email_lbl = QtGui.QLabel("Enter your Gmail")
        self.email_txtLine = QtGui.QLineEdit()
        
        self.startWatcher_btn = QtGui.QPushButton('Start Watcher', self)
        self.startWatcher_btn.clicked.connect(self.startFileWatcher)
        self.startWatcher_btn.setStyleSheet("background-color: #EE3F36")

        self.saveSettings_btn = QtGui.QPushButton('Save Settings', self)
        self.saveSettings_btn.clicked.connect(self.saveSettings)
        
        self.loadSettings_btn = QtGui.QPushButton('Load Settings', self)
        self.loadSettings_btn.clicked.connect(self.loadSettings)
        
        self.delay_spinbox = QtGui.QSpinBox()
        self.delay_spinbox.valueChanged.connect(self.setDelay)
        
        self.groupbox = QtGui.QGroupBox("Settings")
        self.console = QtGui.QPlainTextEdit()

        self.setLayoutOnUI()
        self.setFixedSize(450, 220)
        self.setWindowTitle('FileWatcher')

    def setLayoutOnUI(self):
        mainLayout = QtGui.QVBoxLayout()
        self.setLayout(mainLayout)

        horizontalSpacer_1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        fileWatcherLayout_1 = QtGui.QHBoxLayout()
        fileWatcherLayout_1.addWidget(self.choseFile_btn)
        fileWatcherLayout_1.addItem(horizontalSpacer_1)
        fileWatcherLayout_1.addWidget(self.choseFile_txtLine)

        horizontalSpacer_2 = QtGui.QSpacerItem(16, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        fileWatcherLayout_2 = QtGui.QHBoxLayout()
        fileWatcherLayout_2.addWidget(self.email_lbl)
        fileWatcherLayout_2.addItem(horizontalSpacer_2)
        fileWatcherLayout_2.addWidget(self.email_txtLine)

        groupboxLay = QtGui.QHBoxLayout()
        groupboxLay.addWidget(self.delay_spinbox)
        groupboxLay.addWidget(self.saveSettings_btn)
        groupboxLay.addWidget(self.loadSettings_btn)
        self.groupbox.setLayout(groupboxLay)

        horizontalSpacer_3 = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        fileWatcherLayout_3 = QtGui.QHBoxLayout()
        fileWatcherLayout_3.addWidget(self.groupbox)
        fileWatcherLayout_3.addItem(horizontalSpacer_3)
        fileWatcherLayout_3.addWidget(self.startWatcher_btn)

        fileWatcherLayout_4 = QtGui.QHBoxLayout()
        fileWatcherLayout_4.addWidget(self.console)
        
        mainLayout.addLayout(fileWatcherLayout_1)
        mainLayout.addLayout(fileWatcherLayout_2)
        mainLayout.addLayout(fileWatcherLayout_3)
        mainLayout.addLayout(fileWatcherLayout_4)

    def fileOpen(self):
        path = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        self.path = path
        self.choseFile_txtLine.setText(path)

    def setDelay(self):
        self.delay = self.delay_spinbox.value()

    def startThreadandEmitSignals(self):
        self.writeOnConsole("Start Counter: " + str(self.delay) + " seconds")
        self.threadedEmail = ThreadedEmail(self.path, self.login_email, self.login_password, self.receiver_email, self.delay, False)
        QtCore.QThreadPool.globalInstance().start(self.threadedEmail)

    def writeOnConsole(self, text):
        self.console.appendPlainText(text)

    def startFileWatcher(self):
        self.writeOnConsole("Start watcher")
        self.startWatcher_btn.setStyleSheet("background-color: #2BBE32")
        if not self.isFileWatcherOn:
            # Set up file system watcher
            self.qfsw = QtCore.QFileSystemWatcher()
            self.qfsw.addPaths([self.path])
            QtCore.QObject.connect(self.qfsw, QtCore.SIGNAL("fileChanged(QString)"), self.startThreadandEmitSignals)
            self.isFileWatcherOn = True
        else:
            self.writeOnConsole("File Watcher is already started!")


    def saveSettings(self):
        self.writeOnConsole("Settings Saved")
        self.receiver_email = self.email_txtLine.text()
        self.settings.setValue('login_email', self.login_email)
        self.settings.setValue('login_password', self.login_password)
        self.settings.setValue('receiver_email', self.receiver_email)
        self.settings.setValue('file_path', self.path)
        self.settings.setValue('delay', self.delay)


    def loadSettings(self):
        self.writeOnConsole("Settings Loaded")
        # --> If exists, get setting from *.ini and store in variables, else initialize them
        self.login_email = str(self.settings.value('login_email', '********'))
        self.login_password = str(self.settings.value('login_password', "*********"))
        self.receiver_email = str(self.settings.value('receiver_email', ""))
        self.path = str(self.settings.value('file_path', "********"))
        self.email_txtLine.setText(self.receiver_email)
        self.choseFile_txtLine.setText(self.path)
        self.delay = int(self.settings.value('delay', 10))
        self.delay_spinbox.setValue(self.delay)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = UserInterface()
    window.show()
    sys.exit(app.exec_())
