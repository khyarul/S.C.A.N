"""Programmed by Khyarul Arham"""
########GUI Module#######
from subprocess import Popen
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
########Database Module#########
from pymongo import MongoClient
########MQTT Module#############
import paho.mqtt.client as mqttClient

#################Inisiasi Database#######################
dbClient = MongoClient("mongodb://localhost:27017/")
db = dbClient['ATTENDANCE']
collection = db['NODE']


#################MQTT Callback Event###########################
def on_connect(client, userdata, flags, rc):
    print('Code', str(rc), end=' ')
    if rc == 0:
        # Client.subscribe('UID/Node_' + NODE)
        # Client.subscribe('STATUS/Node_' + NODE, 2)
        print('Connection successful')
    elif rc == 1:
        print('Connection refused - incorrect protocol version')
    elif rc == 2:
        print('Connection refused - invalid client identifier')
    elif rc == 3:
        print('Connection refused - server unavailable')
    elif rc == 4:
        print('Connection refused - bad username or password')
    elif rc == 5:
        print('Connection refused - not authorised')


def on_message(client, userdata, message):
    message.payload = message.payload.decode('utf-8')
    topic = message.topic


###############MQTT global variable####################
client = None
Client = ''
Username = ''
Password = ''
Host = ''
Port = None


#################Inisiasi MQTT###########################


#################Main Window########################
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('S.C.A.N - Node Monitor')
        self.setWindowIcon(QIcon('icons/node.png'))
        self.resize(1000, 300)
        self.setup()
        # self.showMaximized()
        self.show()

    def setup(self):
        self.widget()
        self.layouts()
        self.getNode()

    def widget(self):
        font = QFont()
        font.setPointSize(10)
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.serverConfigLabel = QLabel('MQTT Server Configuration')
        self.serverConfigLabel.setFont(font1)
        self.clientIDInput = QLineEdit()
        self.clientIDInput.setText('NODE MONITOR')
        self.clientIDInput.setPlaceholderText('Client ID')
        self.hostInput = QLineEdit()
        self.hostInput.setPlaceholderText('IP/Hostname')
        self.portInput = QLineEdit()
        self.portInput.setText('1883')
        self.portInput.setPlaceholderText('Port (default: 1883)')
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText('Username')
        self.passInput = QLineEdit()
        self.passInput.setPlaceholderText('Password')
        self.passInput.setEchoMode(QLineEdit.Password)
        self.authCheck = QCheckBox('Use Authentication', self)
        self.toggleAuth()
        self.authCheck.toggled.connect(self.toggleAuth)
        self.connectBtn = QRadioButton('CONNECT')
        self.connectBtn.setStyleSheet('background-color: rgb(122,255,112);')
        self.connectBtn.setIcon(QIcon('icons/connect'))
        self.connectBtn.setFont(font)
        self.connectBtn.setFixedWidth(100)
        self.connectBtn.toggled.connect(self.connectMqtt)
        self.connectStatus = QLabel('DISCONNECTED')

        self.nodeInfoLabel = QLabel('Node Information')
        self.nodeInfoLabel.setFont(font1)
        self.nodeAlias = QLabel()
        self.nodeClient = QLabel()
        self.nodeStatus = QLabel()
        self.nodeDoorStatus = QLabel()
        self.unlockDoorBtn = QPushButton('Unlock Door')
        self.unlockDoorBtn.setIcon(QIcon('icons/unlock'))
        self.unlockDoorBtn.setFont(font)
        self.unlockDoorBtn.setFixedWidth(100)

        self.serverConfigFrame = QFrame()
        self.serverConfigFrame.setStyleSheet('background-color: white;')
        self.serverConfigFrame.setFrameShape(QFrame.Panel)
        self.serverConfigFrame.setFrameShadow(QFrame.Raised)
        self.nodeInfoFrame = QFrame()
        self.nodeInfoFrame.setStyleSheet('background-color: white;')
        self.nodeInfoFrame.setFrameShape(QFrame.Panel)
        self.nodeInfoFrame.setFrameShadow(QFrame.Raised)
        self.logLabel = QLabel('Event Log')
        self.logLabel.setFont(font1)
        self.logList = QListWidget()

        self.nodeLabel = QLabel('Node List')
        self.nodeLabel.setFont(font1)
        self.refreshBtn = QPushButton('PING')
        self.refreshBtn.setIcon(QIcon('icons/refresh.png'))
        self.refreshBtn.setFont(font)
        self.refreshBtn.clicked.connect(self.getNode)
        self.nodeList = QListWidget()
        self.nodeList.itemSelectionChanged.connect(self.showNode)
        self.addBtn = QPushButton('Add')
        self.addBtn.setIcon(QIcon('icons/add.png'))
        self.addBtn.setFont(font)
        self.addBtn.clicked.connect(self.addNode)
        self.editBtn = QPushButton('Edit')
        self.editBtn.setIcon(QIcon('icons/edit.png'))
        self.editBtn.setFont(font)
        self.editBtn.clicked.connect(self.editNode)
        self.deleteBtn = QPushButton('Remove')
        self.deleteBtn.setIcon(QIcon('icons/remove.png'))
        self.deleteBtn.setFont(font)
        self.deleteBtn.clicked.connect(self.deleteNode)
        self.employeeBtn = QPushButton('Employee Manager')
        self.employeeBtn.setIcon(QIcon('icons/person.png'))
        self.employeeBtn.setFont(font)
        self.employeeBtn.clicked.connect(self.openEmployee)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.leftTopLayout = QHBoxLayout()
        self.leftTopLayout1 = QVBoxLayout()
        self.connectLayout = QHBoxLayout()
        self.leftTopLayout2 = QVBoxLayout()
        self.unlockDoorLayout = QHBoxLayout()
        self.leftBotLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightBotLayout = QHBoxLayout()
        self.serverInfo = QGridLayout(self.serverConfigFrame)
        self.serverInfo.setAlignment(Qt.AlignLeft)
        self.nodeInfo = QGridLayout(self.nodeInfoFrame)
        self.nodeInfo.setAlignment(Qt.AlignLeft)

        self.mainLayout.addLayout(self.leftLayout, 77)
        self.mainLayout.addLayout(self.rightLayout, 23)

        self.leftLayout.addLayout(self.leftTopLayout)
        self.leftLayout.addLayout(self.leftBotLayout)
        self.leftLayout.setContentsMargins(0, 0, 10, 0)
        self.leftTopLayout.addLayout(self.leftTopLayout1, 65)
        self.leftTopLayout.addLayout(self.leftTopLayout2, 35)
        self.leftTopLayout.setContentsMargins(0, 0, 0, 10)
        self.leftTopLayout1.addWidget(self.serverConfigLabel)
        self.leftTopLayout1.addWidget(self.serverConfigFrame)
        self.leftTopLayout1.setContentsMargins(0, 0, 10, 0)
        self.leftTopLayout1.addLayout(self.connectLayout)
        self.connectLayout.addStretch()
        self.connectLayout.addWidget(self.connectBtn)
        self.connectLayout.addWidget(self.connectStatus)
        self.connectLayout.addStretch()
        self.leftTopLayout2.addWidget(self.nodeInfoLabel)
        self.leftTopLayout2.addWidget(self.nodeInfoFrame)
        self.leftTopLayout2.addLayout(self.unlockDoorLayout)
        self.unlockDoorLayout.addStretch()
        self.unlockDoorLayout.addWidget(self.unlockDoorBtn)
        self.unlockDoorLayout.addStretch()
        self.leftBotLayout.addWidget(self.logLabel)
        self.leftBotLayout.addWidget(self.logList)

        self.rightTopLayout.addWidget(self.nodeLabel)
        self.rightTopLayout.addWidget(self.refreshBtn)
        self.rightTopLayout.addStretch()
        self.rightLayout.addLayout(self.rightTopLayout)
        self.rightLayout.addWidget(self.nodeList)
        self.rightLayout.addLayout(self.rightBotLayout)
        self.rightLayout.addWidget(self.employeeBtn)

        self.serverInfo.addWidget(QLabel('Client ID'), 0, 0)
        self.serverInfo.addWidget(QLabel(':'), 0, 1)
        self.serverInfo.addWidget(self.clientIDInput, 0, 2)
        self.serverInfo.addWidget(QLabel('Server/Host'), 1, 0)
        self.serverInfo.addWidget(QLabel(':'), 1, 1)
        self.serverInfo.addWidget(self.hostInput, 1, 2)
        self.serverInfo.addWidget(QLabel('Port'), 2, 0)
        self.serverInfo.addWidget(QLabel(':'), 2, 1)
        self.serverInfo.addWidget(self.portInput, 2, 2)
        self.serverInfo.addWidget(self.authCheck, 0, 5)
        self.serverInfo.addWidget(QLabel('   Username'), 1, 3)
        self.serverInfo.addWidget(QLabel(':'), 1, 4)
        self.serverInfo.addWidget(self.usernameInput, 1, 5)
        self.serverInfo.addWidget(QLabel('   Password'), 2, 3)
        self.serverInfo.addWidget(QLabel(':'), 2, 4)
        self.serverInfo.addWidget(self.passInput, 2, 5)

        self.nodeInfo.addWidget(QLabel('Alias'), 0, 0)
        self.nodeInfo.addWidget(QLabel(':'), 0, 1)
        self.nodeInfo.addWidget(self.nodeAlias, 0, 2)
        self.nodeInfo.addWidget(QLabel('Client ID'), 1, 0)
        self.nodeInfo.addWidget(QLabel(':'), 1, 1)
        self.nodeInfo.addWidget(self.nodeClient, 1, 2)
        self.nodeInfo.addWidget(QLabel('Connection Status'), 2, 0)
        self.nodeInfo.addWidget(QLabel(':'), 2, 1)
        self.nodeInfo.addWidget(self.nodeStatus, 2, 2)
        self.nodeInfo.addWidget(QLabel('Door Status'), 3, 0)
        self.nodeInfo.addWidget(QLabel(':'), 3, 1)
        self.nodeInfo.addWidget(self.nodeDoorStatus, 3, 2)

        self.rightBotLayout.addWidget(self.addBtn)
        self.rightBotLayout.addWidget(self.editBtn)
        self.rightBotLayout.addWidget(self.deleteBtn)

        self.setLayout(self.mainLayout)

    def getNode(self):
        self.nodeList.clear()
        list = collection.find().sort('Alias', 1)
        for x in list:
            self.nodeList.addItem(x['Alias'] + ' - ' + x['Client ID'])
        self.nodeList.setCurrentRow(0)  # atur kursor ke item pertama

    def showNode(self):
        try:
            self.nodeAlias.setText('')
            self.nodeClient.setText('')
            self.nodeStatus.setText('')
            self.nodeDoorStatus.setText('')

            data = self.nodeList.currentItem().text()
            clientID = data.split(' - ')[1]
            list = collection.find({'Client ID': clientID})
            for x in list: pass
            self.nodeAlias.setText(x['Alias'])
            self.nodeClient.setText(x['Client ID'])
        except:
            QMessageBox.information(self, 'WARNING', 'This Node is no longer available on Database')

    def addNode(self):
        self.newNode = AddNode()

    def editNode(self):
        pass

    def deleteNode(self):
        if self.nodeList.selectedItems():
            data = self.nodeList.currentItem().text()
            clientID = data.split(' - ')[1]
            message = QMessageBox.question(self, 'WARNING', 'Are you sure want to remove this Node?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                try:
                    collection.delete_one({'Client ID': clientID})
                    QMessageBox.information(self, 'SUCCESS', 'This Node has been removed')
                    self.getNode()
                except:
                    QMessageBox.information(self, 'WARNING', 'This Node is no longer available')
        else:
            QMessageBox.information(self, 'WARNING', 'Please select a Node to remove')

    def toggleAuth(self):
        if self.authCheck.isChecked():
            self.usernameInput.setEnabled(True)
            self.passInput.setEnabled(True)
        else:
            self.usernameInput.setEnabled(False)
            self.passInput.setEnabled(False)

    def connectMqtt(self):
        global client
        Client = self.clientIDInput.text()
        Username = self.usernameInput.text()
        Password = self.passInput.text()
        Host = self.hostInput.text()
        Port = self.portInput.text()
        if self.connectBtn.isChecked():
            client = mqttClient.Client(Client)
            if self.authCheck.isChecked():
                client.username_pw_set(Username, Password)
            client.on_message = on_message
            client.on_connect = on_connect
            try:
                client.connect(Host, int(Port), 60)
                client.loop_start()
                self.connectStatus.setText('CONNECTED')
            except:
                print('Connection Failed')
                self.connectBtn.setChecked(False)
                self.connectStatus.setText('DISCONNECTED')
        else:
            client.disconnect()
            self.connectStatus.setText('DISCONNECTED')

    def openEmployee(self):
        Popen('python karyawan.py')
        # os.system('python karyawan.py')
        # call(['python', 'karyawan.py'])


################################################################################
class AddNode(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Node')
        # self.setWindowIcon(QIcon('icons/person.png'))
        self.resize(300, 100)
        self.setup()
        self.show()

    def setup(self):
        self.widget()
        self.layouts()

    def widget(self):
        self.aliasLabel = QLabel('Alias')
        self.clientLabel = QLabel('Client ID')
        self.aliasInput = QLineEdit()
        self.aliasInput.setPlaceholderText('Alias (Can be location name or something)')
        self.clientInput = QLineEdit()
        self.clientInput.setText('Node_')
        self.clientInput.setPlaceholderText('Should be unique')
        self.addBtn = QPushButton('Add Node')
        self.addBtn.setFixedWidth(100)
        self.addBtn.clicked.connect(self.addFunc)

    def layouts(self):
        ##########################LAYOUT###############################
        self.mainLayout = QGridLayout()
        ###################Tambah Widget ke Layout#####################
        self.mainLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.addWidget(self.aliasLabel, 0, 0)
        self.mainLayout.addWidget(QLabel(':'), 0, 1)
        self.mainLayout.addWidget(self.aliasInput, 0, 2)
        self.mainLayout.addWidget(self.clientLabel, 1, 0)
        self.mainLayout.addWidget(QLabel(':'), 1, 1)
        self.mainLayout.addWidget(self.clientInput, 1, 2)
        self.mainLayout.addWidget(self.addBtn, 2, 2)
        ##################Atur Main Windows Layout#####################
        self.setLayout(self.mainLayout)

    def addFunc(self):
        Alias = self.aliasInput.text()
        ClientID = self.clientInput.text()

        result_count = collection.count_documents({'Client ID': ClientID})
        if Alias and ClientID != '':
            if result_count == 0:
                data = {'Alias': Alias, 'Client ID': ClientID}
                collection.insert_one(data)
                QMessageBox.information(self, 'SUCCESS', 'New Node has been added')
                w.getNode()
            else:
                QMessageBox.information(self, 'WARNING', 'Client ID already exist, try again')
        else:
            QMessageBox.information(self, 'WARNING', 'Fields can not be empty')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
