"""Programmed by Khyarul Arham"""
########GUI Module#######
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
########Database Module#########
from pymongo import MongoClient

#######################################################################

newPath = 'images/person.png'
globalID = None

dbClient = MongoClient("mongodb://localhost:27017/")
db = dbClient['ATTENDANCE']
collection = db['KARYAWAN']


################################################################################################################################
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('S.C.A.N - Employee Manager')
        self.setWindowIcon(QIcon('icons/person.png'))
        self.resize(600, 500)
        self.setup()
        # self.showMaximized()
        self.show()

    def setup(self):
        self.widget()
        self.layouts()
        self.getKaryawan()

    def widget(self):
        self.setStyleSheet('font-size:11pt;font-family:Arial Bold;')
        #############Daftar Widget################
        self.karyawanList = QListWidget()
        self.karyawanList.itemSelectionChanged.connect(self.showKaryawan)
        self.karyawanList.doubleClicked.connect(self.editKaryawan)
        # self.refreshButton = QPushButton('Refresh')
        # self.refreshButton.setStyleSheet('background-color:green;font-size:10;')
        self.addButton = QPushButton('Add')
        self.addButton.setStyleSheet('background-color:orange;font-size:10;')
        self.editButton = QPushButton('Edit')
        self.editButton.setStyleSheet('background-color:orange;font-size:10;')
        self.deleteButton = QPushButton('Delete')
        self.deleteButton.setStyleSheet('background-color:orange;font-size:10;')
        ##########################################
        self.addButton.clicked.connect(self.addKaryawan)
        # self.refreshButton.clicked.connect(self.getKaryawan)
        self.editButton.clicked.connect(self.editKaryawan)
        self.deleteButton.clicked.connect(self.deleteKaryawan)

    def layouts(self):
        #############Daftar Layout################
        self.mainLayout = QHBoxLayout()
        frame = QFrame()
        frame.setStyleSheet('background-color: rgb(245,255,250);')
        frame.setFrameShape(QFrame.Panel)
        frame.setFrameShadow(QFrame.Raised)
        scroll = QScrollArea()
        # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(frame)
        self.leftMainLayout = QFormLayout(frame)
        self.rightMainLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightBotLayout = QHBoxLayout()
        ##############tambah Child Layout ke Main Layout###############
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBotLayout)
        self.mainLayout.addWidget(scroll, 50)
        self.mainLayout.addLayout(self.rightMainLayout, 50)
        ##############tambah Widget ke Layout##########################
        self.rightTopLayout.addWidget(self.karyawanList)
        # self.rightBotLayout.addWidget(self.refreshButton)
        self.rightBotLayout.addWidget(self.addButton)
        self.rightBotLayout.addWidget(self.editButton)
        self.rightBotLayout.addWidget(self.deleteButton)
        ##############Atur Main Window Layout##########################
        self.setLayout(self.mainLayout)

    def addKaryawan(self):
        self.newKaryawan = AddKaryawan()

    def getKaryawan(self):
        self.karyawanList.clear()
        count = 0
        list = collection.find().sort('Name', 1)
        for x in list:
            count += 1
            self.karyawanList.addItem(str(count) + '. ' + x['Name'] + ' - ' + x['UID'])
        self.karyawanList.setCurrentRow(0)  # atur kursor ke item pertama

    def showKaryawan(self):
        try:
            for i in reversed(range(self.leftMainLayout.count())):
                widget = self.leftMainLayout.takeAt(i).widget()
                if widget != None:
                    widget.deleteLater()

            data = self.karyawanList.currentItem().text()
            id = data.split(' - ')[1]
            list = collection.find({'UID': id})
            for x in list: pass
            img = QLabel()
            img.setPixmap(QPixmap(x['Picture']).scaled(128, 128))
            img.setFrameShape(QFrame.StyledPanel)
            img.setFrameShadow(QFrame.Sunken)
            img.setFixedWidth(128)
            img.setStyleSheet('background-color: white')
            font = QFont()
            font.setBold(True)
            UID = QLabel(x['UID'])
            UID.setFont(font)
            UID.setFrameShape(QFrame.WinPanel)
            UID.setFrameShadow(QFrame.Sunken)
            UID.setStyleSheet('background-color: white')
            Name = QLabel(x['Name'])
            Name.setFont(font)
            Name.setFrameShape(QFrame.WinPanel)
            Name.setFrameShadow(QFrame.Sunken)
            Name.setStyleSheet('background-color: white')
            Phone = QLabel(x['Phone'])
            Phone.setFont(font)
            Phone.setFrameShape(QFrame.WinPanel)
            Phone.setFrameShadow(QFrame.Sunken)
            Phone.setStyleSheet('background-color: white')
            Email = QLabel(x['Email'])
            Email.setFont(font)
            Email.setFrameShape(QFrame.WinPanel)
            Email.setFrameShadow(QFrame.Sunken)
            Email.setStyleSheet('background-color: white')
            Address = QLabel(x['Address'])
            Address.setWordWrap(True)
            Address.setFont(font)
            Address.setFrameShape(QFrame.WinPanel)
            Address.setFrameShadow(QFrame.Sunken)
            Address.setStyleSheet('background-color: white')
            self.leftMainLayout.setVerticalSpacing(10)
            self.leftMainLayout.addRow('', img)
            self.leftMainLayout.addRow('UID', UID)
            self.leftMainLayout.addRow('Full Name', Name)
            self.leftMainLayout.addRow('Phone', Phone)
            self.leftMainLayout.addRow('E-mail', Email)
            self.leftMainLayout.addRow('Address', Address)
        except:
            QMessageBox.information(self, 'WARNING', 'This Person is no longer available on Database')

    def deleteKaryawan(self):
        if self.karyawanList.selectedItems():
            data = self.karyawanList.currentItem().text()
            id = data.split(' - ')[1]
            message = QMessageBox.question(self, 'WARNING', 'Are you sure want to delete this person?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                try:
                    collection.delete_one({'UID': id})
                    QMessageBox.information(self, 'SUCCESS', 'This Person has been deleted')
                    self.getKaryawan()
                except:
                    QMessageBox.information(self, 'WARNING', 'This Person is no longer available')
        else:
            QMessageBox.information(self, 'WARNING', 'Please select a person to delete')

    def editKaryawan(self):
        try:
            global globalID
            if self.karyawanList.selectedItems():
                data = self.karyawanList.currentItem().text()
                globalID = data.split(' - ')[1]
                self.editWindow = EditKaryawan()
            else:
                QMessageBox.information(self, 'WARNING', 'Please select a person to edit')
        except:
            QMessageBox.information(self, 'WARNING', 'This Person is no longer available on Database')


################################################################################################################################
class EditKaryawan(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Employee')
        self.setWindowIcon(QIcon('icons/person.png'))
        self.resize(400, 500)
        self.setup()
        self.show()

    def setup(self):
        self.getPerson()
        self.widget()
        self.layouts()

    def widget(self):
        #############top widget###################
        self.setStyleSheet('font-size:11pt;font-family:Arial Bold;')
        # self.title = QLabel('Update Employee')
        self.newPersonImg = QLabel()
        self.newPersonImg.setPixmap(QPixmap(self.Picture).scaled(128, 128))
        self.picButton = QPushButton('Browse Picture')
        self.picButton.setStyleSheet('background-color:orange;font-size:10;')
        self.picButton.clicked.connect(self.browsePic)
        #############bottom widget################
        font = QFont()
        font.setBold(True)
        self.uidLabel = QLabel('UID')
        self.uidLabel.setFont(font)
        self.uidInput = QLineEdit()
        self.uidInput.setPlaceholderText('UID without space, example: c8f3ff92 or C8F3FF92, from RFID tag')
        self.uidInput.setText(self.UID)
        self.nameLabel = QLabel('Full Name')
        self.nameLabel.setFont(font)
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText('Enter Full Name')
        self.nameInput.setText(self.Name)
        self.phoneLabel = QLabel('Phone')
        self.phoneLabel.setFont(font)
        self.phoneInput = QLineEdit()
        self.phoneInput.setPlaceholderText('08xxxxxxxxxx')
        self.phoneInput.setText(self.Phone)
        self.emailLabel = QLabel('E-mail')
        self.emailLabel.setFont(font)
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText('Enter E-mail')
        self.emailInput.setText(self.Email)
        self.addressLabel = QLabel('Address')
        self.addressLabel.setFont(font)
        self.addressInput = QTextEdit()
        self.addressInput.setText(self.Address)
        self.updateButton = QPushButton('Update Employee')
        self.updateButton.setFont(font)
        self.updateButton.setStyleSheet('background-color:orange;font-size:10;')
        self.updateButton.clicked.connect(self.updateFunc)

    def layouts(self):
        #############Daftar Layout################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        ##############tambah Child Layout ke Main Layout###############
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ##############tambah Widget ke Layout##########################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.newPersonImg)
        self.topLayout.addWidget(self.picButton)
        self.topLayout.addStretch()
        # self.setContentsMargins() #left, top, right, bottom
        self.bottomLayout.addRow(self.uidLabel, self.uidInput)
        self.bottomLayout.addRow(self.nameLabel, self.nameInput)
        self.bottomLayout.addRow(self.phoneLabel, self.phoneInput)
        self.bottomLayout.addRow(self.emailLabel, self.emailInput)
        self.bottomLayout.addRow(self.addressLabel, self.addressInput)
        self.bottomLayout.addRow('', self.updateButton)
        ##############Atur Main Window Layout##########################
        self.setLayout(self.mainLayout)

    def getPerson(self):
        global globalID, newPath
        list = collection.find({'UID': globalID})
        for x in list: pass
        self.UID = x['UID']
        self.Name = x['Name']
        self.Phone = x['Phone']
        self.Email = x['Email']
        self.Address = x['Address']
        self.Picture = x['Picture']
        newPath = self.Picture

    def browsePic(self):
        global newPath
        self.fileName, ok = QFileDialog.getOpenFileName(self, 'Browse Picture', '', 'Images Files(*.jpg *.png)')
        if ok:
            defaultImg = os.path.basename(self.fileName)  # ambil nama file
            img = Image.open(self.fileName)  # baca path file
            newPath = 'images/{}'.format(defaultImg)  # buat path baru
            img.save(newPath)  # simpan ke directory project
            self.newPersonImg.setPixmap(QPixmap(newPath).scaled(128, 128))  # tampilkan foto

    def updateFunc(self):
        UID = self.uidInput.text().upper()
        Name = self.nameInput.text()
        Phone = self.phoneInput.text()
        Email = self.emailInput.text()
        Address = self.addressInput.toPlainText()
        Picture = newPath

        if UID and Name and Phone and Email and Address != '':
            global globalID
            data = {'UID': UID, 'Name': Name, 'Picture': Picture, 'Phone': Phone, 'Email': Email, 'Address': Address}
            query = {'UID': globalID}
            newValue = {'$set': data}
            collection.update_one(query, newValue)
            QMessageBox.information(self, 'SUCCESS', 'The Employee has been updated')
            w.getKaryawan()
        else:
            QMessageBox.information(self, 'WARNING', 'Fields can not be empty')


################################################################################################################################
class AddKaryawan(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Employee')
        self.setWindowIcon(QIcon('icons/person.png'))
        self.resize(400, 500)
        self.setup()
        self.show()

    def setup(self):
        self.widget()
        self.layouts()

    def widget(self):
        global newPath
        newPath = 'images/person.png'
        #############top widget###################
        self.setStyleSheet('font-size:11pt;font-family:Arial Bold;')
        # self.title = QLabel('Add Employee')
        self.newPersonImg = QLabel()
        self.newPersonImg.setPixmap(QPixmap(newPath))
        self.picButton = QPushButton('Browse Picture')
        self.picButton.setStyleSheet('background-color:orange;font-size:10;')
        self.picButton.clicked.connect(self.browsePic)
        #############bottom widget################
        font = QFont()
        font.setBold(True)
        self.uidLabel = QLabel('UID')
        self.uidLabel.setFont(font)
        self.uidInput = QLineEdit()
        self.uidInput.setPlaceholderText('UID without space, example: c8f3ff92 or C8F3FF92, from RFID tag')
        self.nameLabel = QLabel('Full Name')
        self.nameLabel.setFont(font)
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText('Enter Full Name')
        self.phoneLabel = QLabel('Phone')
        self.phoneLabel.setFont(font)
        self.phoneInput = QLineEdit()
        self.phoneInput.setPlaceholderText('08xxxxxxxxxx')
        self.emailLabel = QLabel('E-mail')
        self.emailLabel.setFont(font)
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText('Enter E-mail')
        self.addressLabel = QLabel('Address')
        self.addressLabel.setFont(font)
        self.addressInput = QTextEdit()
        self.addButton = QPushButton('Add Employee')
        self.addButton.setFont(font)
        self.addButton.setStyleSheet('background-color:orange;font-size:10;')
        self.addButton.clicked.connect(self.addFunc)

    def layouts(self):
        #############Daftar Layout################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        ##############tambah Child Layout ke Main Layout###############
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ##############tambah Widget ke Layout##########################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.newPersonImg)
        self.topLayout.addWidget(self.picButton)
        self.topLayout.addStretch()
        # self.setContentsMargins() #left, top, right, bottom
        self.bottomLayout.addRow(self.uidLabel, self.uidInput)
        self.bottomLayout.addRow(self.nameLabel, self.nameInput)
        self.bottomLayout.addRow(self.phoneLabel, self.phoneInput)
        self.bottomLayout.addRow(self.emailLabel, self.emailInput)
        self.bottomLayout.addRow(self.addressLabel, self.addressInput)
        self.bottomLayout.addRow('', self.addButton)
        ##############Atur Main Window Layout##########################
        self.setLayout(self.mainLayout)

    def browsePic(self):
        global newPath
        self.fileName, ok = QFileDialog.getOpenFileName(self, 'Browse Picture', '', 'Images Files(*.jpg *.png)')
        if ok:
            defaultImg = os.path.basename(self.fileName)  # ambil nama file
            img = Image.open(self.fileName)  # baca path file
            newPath = 'images/{}'.format(defaultImg)  # buat path baru
            img.save(newPath)  # simpan ke directory project
            self.newPersonImg.setPixmap(QPixmap(newPath).scaled(128, 128))  # tampilkan foto

    def addFunc(self):
        UID = self.uidInput.text().upper()
        Name = self.nameInput.text()
        Picture = newPath
        Phone = self.phoneInput.text()
        Email = self.emailInput.text()
        Address = self.addressInput.toPlainText()

        query = {'UID': UID}
        result_count = collection.count_documents(query)

        if UID and Name and Phone and Email and Address != '':
            if result_count == 0:
                data = {'UID': UID, 'Name': Name, 'Picture': Picture, 'Phone': Phone, 'Email': Email,
                        'Address': Address}
                collection.insert_one(data)
                QMessageBox.information(self, 'SUCCESS', 'New Employee has been added')
                w.getKaryawan()
            else:
                QMessageBox.information(self, 'WARNING', 'The UID already exists')
        else:
            QMessageBox.information(self, 'WARNING', 'Fields can not be empty')


################################################################################################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
