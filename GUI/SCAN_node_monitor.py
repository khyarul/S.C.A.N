"""Programmed by Khyarul Arham"""
########GUI Module#######
from subprocess import Popen, PIPE
import sys
import platform
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PIL import Image
########Database Module#########
from pymongo import MongoClient
########MQTT Module#############
import paho.mqtt.client as mqttClient
################################
import threading
import time
from datetime import datetime

#################Inisiasi Database#######################
dbClient = MongoClient("mongodb://localhost:27017/")
db = dbClient['ATTENDANCE']
nodeCollection = db['NODE']
employeeCollection = db['KARYAWAN']
nodeID = None
#################MQTT Callback Event###########################
RC = -1


def on_connect(client, userdata, flags, rc):
    # print('Code', str(rc), end=' ')
    global RC
    RC = rc
    if rc == 0:
        pass
    # print('Connection successful')
    elif rc == 1:
        pass
    # print('Connection refused - incorrect protocol version')
    elif rc == 2:
        pass
    # print('Connection refused - invalid client identifier')
    elif rc == 3:
        pass
    # print('Connection refused - server unavailable')
    elif rc == 4:
        pass
    # print('Connection refused - bad username or password')
    elif rc == 5:
        pass
    # print('Connection refused - not authorised')


TOPIC = None
PAYLOAD = None


def on_message(client, userdata, message):
    global TOPIC, PAYLOAD
    PAYLOAD = message.payload = message.payload.decode('utf-8')
    TOPIC = message.topic


###############MQTT global variable####################
client = None
Client = ''
Username = ''
Password = ''
Host = ''
Port = None
nodeStatusVar = {}
doorStatusVar = {}

#################Inisiasi MQTT###########################
client = mqttClient.Client(Client)


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
        self.connectBtn.setStyleSheet('background-color: rgb(122, 255, 112);')
        self.connectBtn.setIcon(QIcon('icons/connect'))
        self.connectBtn.setFont(font)
        self.connectBtn.setFixedWidth(110)
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
        self.unlockDoorBtn.clicked.connect(self.unlockDoor)
        self.unlockDoorBtn.setDisabled(True)

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
        self.pingBtn = QPushButton('PING')
        self.pingBtn.setIcon(QIcon('icons/ping.png'))
        self.pingBtn.setFont(font)
        self.pingBtn.clicked.connect(self.getNode)
        self.nodeList = QListWidget()
        self.nodeList.itemSelectionChanged.connect(self.showNode)
        self.nodeList.doubleClicked.connect(self.editNode)
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
        self.rightTopLayout.addWidget(self.pingBtn)
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

    def enableConfig(self, command):
        self.clientIDInput.setEnabled(command)
        self.hostInput.setEnabled(command)
        self.portInput.setEnabled(command)
        self.usernameInput.setEnabled(command)
        self.passInput.setEnabled(command)
        self.authCheck.setEnabled(command)

    def getNode(self):
        self.nodeList.clear()
        list = nodeCollection.find().sort('Alias', 1)
        for x in list:
            self.nodeList.addItem(x['Alias'] + ' - ' + x['Client ID'])
        self.nodeList.setCurrentRow(0)  # atur kursor ke item pertama

    def showNode(self):
        try:
            data = self.nodeList.currentItem().text()
            clientID = data.split(' - ')[1]
            clientAlias = data.split(' - ')[0]

            self.nodeAlias.setText(clientAlias)
            self.nodeClient.setText(clientID)
            self.nodeStatus.setText('')
            self.nodeDoorStatus.setText('')
            try:
                if nodeStatusVar[clientID] == '1':
                    self.nodeStatus.setText('CONNECTED')
                    self.nodeStatus.setStyleSheet('color:green')
                elif nodeStatusVar[clientID] == '0':
                    self.nodeStatus.setText('DISCONNECTED')
                    self.nodeStatus.setStyleSheet('color:red')
                if doorStatusVar[clientID] == '1':
                    self.nodeDoorStatus.setText('OPENED')
                    self.nodeDoorStatus.setStyleSheet('color:green')
                elif doorStatusVar[clientID] == '0':
                    self.nodeDoorStatus.setText('CLOSED')
                    self.nodeDoorStatus.setStyleSheet('color:red')
            except:
                pass
        except:
            QMessageBox.information(self, 'WARNING', 'This Node is no longer available on Database')

    def refreshNode(self):
        global nodeStatusVar, doorStatusVar
        data = self.nodeList.currentItem().text()
        clientID = data.split(' - ')[1]
        self.nodeStatus.setText('')
        self.nodeDoorStatus.setText('')
        try:
            if nodeStatusVar[clientID] == '1':
                self.nodeStatus.setText('CONNECTED')
                self.nodeStatus.setStyleSheet('color:green')
            elif nodeStatusVar[clientID] == '0':
                self.nodeStatus.setText('DISCONNECTED')
                self.nodeStatus.setStyleSheet('color:red')
            if doorStatusVar[clientID] == '1':
                self.nodeDoorStatus.setText('OPENED')
                self.nodeDoorStatus.setStyleSheet('color:green')
            elif doorStatusVar[clientID] == '0':
                self.nodeDoorStatus.setText('CLOSED')
                self.nodeDoorStatus.setStyleSheet('color:red')
        except:
            pass

    def addNode(self):
        self.newNode = AddNode()

    def editNode(self):
        try:
            global nodeID
            if self.nodeList.selectedItems():
                data = self.nodeList.currentItem().text()
                nodeID = data.split(' - ')[1]
                self.editnode = EditNode()
            else:
                QMessageBox.information(self, 'WARNING', 'Please select a Node to edit')
        except:
            QMessageBox.information(self, 'WARNING', 'This Node is no longer available on Database')

    def deleteNode(self):
        if self.nodeList.selectedItems():
            data = self.nodeList.currentItem().text()
            clientID = data.split(' - ')[1]
            message = QMessageBox.question(self, 'WARNING', 'Are you sure want to remove this Node?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                try:
                    nodeCollection.delete_one({'Client ID': clientID})
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
        global client, RC
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
                RC = -1
                client.connect(Host, int(Port), 60)
                client.loop_start()
                self.connectStatus.setText('CONNECTED')
                now = datetime.now()
                date = now.strftime('%d/%m/%Y')
                clock = now.strftime('%H:%M:%S')
                item = self.logList.findItems(date, Qt.MatchExactly)
                if len(item) == 0:
                    self.logList.addItem(date)
                self.logList.addItem(clock + ' CONNECTED to ' + Host + ':' + Port)
                for x in range(self.nodeList.count()):
                    data = self.nodeList.item(x).text()
                    clientID = data.split(' - ')[1]
                    client.subscribe('STATUS/' + clientID)
                    client.subscribe('UID/' + clientID)
                    client.subscribe('DOOR/' + clientID)
                    connectThread = threading.Thread(target=self.connectThreadFunc, args=[clientID])
                    connectThread.start()
                pingThread = threading.Thread(target=self.pingFunc)
                pingThread.start()
                client.subscribe('PERIOD')
                periodThread = threading.Thread(target=self.periodFunc)
                periodThread.start()
                self.enableConfig(False)
                self.unlockDoorBtn.setEnabled(True)
            except:
                client.disconnect()
                self.connectBtn.setChecked(False)
                self.connectStatus.setText('DISCONNECTED')
                self.enableConfig(True)
                self.unlockDoorBtn.setDisabled(True)
        else:
            client.disconnect()
            self.connectStatus.setText('DISCONNECTED')
            self.nodeStatus.setText('')
            self.nodeDoorStatus.setText('')
            now = datetime.now()
            date = now.strftime('%d/%m/%Y')
            clock = now.strftime('%H:%M:%S')
            item = self.logList.findItems(date, Qt.MatchExactly)
            if len(item) == 0:
                self.logList.addItem(date)
            self.logList.addItem(clock + ' DISCONNECTED from ' + Host + ':' + Port + ' RC=' + str(RC))
            self.enableConfig(True)
            self.unlockDoorBtn.setDisabled(True)
            RC = -1

    def openEmployee(self):
        if platform.system() == 'Linux':
            Popen('python3 karyawan.py', shell=True, stdout=PIPE)
        else:
            Popen('python karyawan.py', shell=True, stdout=PIPE)
        # os.system('python karyawan.py')
        # call(['python', 'karyawan.py'])

    def connectThreadFunc(self, clientID):
        global client, TOPIC, PAYLOAD, nodeStatusVar, doorStatusVar, RC
        while True:
            now = datetime.now()
            date = now.strftime('%d/%m/%Y')
            if TOPIC == ('UID/' + clientID):
                ######Read data from topic 'UID/node_x'########
                mode = PAYLOAD.split(':')[0]  # MODE STRING
                uid = PAYLOAD.split(':')[1]  # UID STRING
                query = {'UID': uid}
                resultCount = employeeCollection.count_documents(query)
                #########UNLOCK DOOR MODE##########
                if mode == '0':
                    if resultCount == 0:  # if no matching uid send 0
                        client.publish('RESPON/' + clientID, '0')
                        ########Add to log##########
                        item = self.logList.findItems(date, Qt.MatchExactly)
                        if len(item) == 0:
                            self.logList.addItem(date)
                        clock = now.strftime('%H:%M:%S')
                        message = '{} UNKNOWN UID:{}, trying to unlock door at {}'.format(clock, uid, clientID)
                        self.logList.addItem(message)
                    elif resultCount == 1:  # MATCH Unique UID on database send back 'name'
                        for x in employeeCollection.find(query):
                            name = x['Name']
                        client.publish('RESPON/' + clientID, name)
                        ########Add to log##########
                        item = self.logList.findItems(date, Qt.MatchExactly)
                        if len(item) == 0:
                            self.logList.addItem(date)
                        clock = now.strftime('%H:%M:%S')
                        message = '{} UID:{} Name:{}, unlock door at {}'.format(clock, uid, name, clientID)
                        self.logList.addItem(message)
                #########ATTENDANCE MODE##########
                elif mode == '1':
                    if resultCount == 0:  # if no matching uid send 0
                        client.publish('RESPON/' + clientID, '0')
                        ########Add to log##########
                        item = self.logList.findItems(date, Qt.MatchExactly)
                        if len(item) == 0:
                            self.logList.addItem(date)
                        clock = now.strftime('%H:%M:%S')
                        message = '{} UNKNOWN UID:{}, trying to attend at {}'.format(clock, uid, clientID)
                        self.logList.addItem(message)
                    elif resultCount == 1:  # MATCH Unique UID on database send back 'name'
                        clock = now.strftime('%H:%M')
                        for x in employeeCollection.find(query):
                            name = x['Name']
                        if date in x:  # If person has attend
                            x[date][1] = clock
                        else:  # if person has not attend
                            x[date] = [clock, None]
                        newValue = {'$set': x}
                        employeeCollection.update_one(query, newValue)
                        client.publish('RESPON/' + clientID, name)
                        ########Add to log##########
                        item = self.logList.findItems(date, Qt.MatchExactly)
                        if len(item) == 0:
                            self.logList.addItem(date)
                        clock = now.strftime('%H:%M:%S')
                        message = '{} UID:{} Name:{}, attend at {}'.format(clock, uid, name, clientID)
                        self.logList.addItem(message)
                TOPIC = None
                PAYLOAD = None
            if TOPIC == ('STATUS/' + clientID):
                nodeStatusVar[clientID] = PAYLOAD
                self.refreshNode()
                TOPIC = None
                PAYLOAD = None
            if TOPIC == ('DOOR/' + clientID):
                doorStatusVar[clientID] = PAYLOAD
                self.refreshNode()
                item = self.logList.findItems(date, Qt.MatchExactly)
                if len(item) == 0:
                    self.logList.addItem(date)
                clock = now.strftime('%H:%M:%S')
                if PAYLOAD == '1':
                    message = '{} DOOR OPENED at {}'.format(clock, clientID)
                elif PAYLOAD == '0':
                    message = '{} DOOR CLOSED at {}'.format(clock, clientID)
                self.logList.addItem(message)
                TOPIC = None
                PAYLOAD = None
            if self.connectBtn.isChecked() == False or RC > 0:
                client.disconnect()
                self.connectBtn.setChecked(False)
                self.connectStatus.setText('DISCONNECTED')
                nodeStatusVar[clientID] = None
                break

    def pingFunc(self):
        global client, RC
        while True:
            now = datetime.now()
            date = now.strftime('%a,%d/%b')
            clock = now.strftime(' %H:%M')
            client.publish('TIME', date + clock)
            client.publish('PING', 'ping')
            if self.connectBtn.isChecked() == False or RC > 0:
                # RC = -1
                client.disconnect()
                self.connectBtn.setChecked(False)
                self.connectStatus.setText('DISCONNECTED')
                break
            time.sleep(5)

    def periodFunc(self):
        global TOPIC, PAYLOAD, client
        while True:
            now = datetime.now()
            date = now.strftime('%d/%m/%Y')
            if TOPIC == 'PERIOD':
                item = self.logList.findItems(date, Qt.MatchExactly)
                if len(item) == 0:
                    self.logList.addItem(date)
                message = '                  time needed for authentication flow: {} ms'.format(PAYLOAD)
                self.logList.addItem(message)
                TOPIC = None
                PAYLOAD = None
            if self.connectBtn.isChecked() == False or RC > 0:
                # RC = -1
                client.disconnect()
                self.connectBtn.setChecked(False)
                self.connectStatus.setText('DISCONNECTED')
                break

    def unlockDoor(self):
        global client
        data = self.nodeList.currentItem().text()
        clientID = data.split(' - ')[1]
        client.publish('LOCK/' + clientID, 0)


################################################################################
class AddNode(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Node')
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

        result_count = nodeCollection.count_documents({'Client ID': ClientID})
        if Alias and ClientID != '':
            if result_count == 0:
                data = {'Alias': Alias, 'Client ID': ClientID}
                nodeCollection.insert_one(data)
                QMessageBox.information(self, 'SUCCESS', 'New Node has been added')
                w.getNode()
            else:
                QMessageBox.information(self, 'WARNING', 'Client ID already exist, try again')
        else:
            QMessageBox.information(self, 'WARNING', 'Fields can not be empty')


################################################################################
class EditNode(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Node')
        self.resize(300, 100)
        self.setup()
        self.show()

    def setup(self):
        self.getNode()
        self.widget()
        self.layouts()

    def widget(self):
        self.aliasLabel = QLabel('Alias')
        self.clientLabel = QLabel('Client ID')
        self.aliasInput = QLineEdit()
        self.aliasInput.setText(self.alias)
        self.aliasInput.setPlaceholderText('Alias (Can be location name or something)')
        self.clientInput = QLineEdit()
        self.clientInput.setText(self.clientId)
        self.clientInput.setPlaceholderText('Should be unique')
        self.addBtn = QPushButton('Update Node')
        self.addBtn.setFixedWidth(100)
        self.addBtn.clicked.connect(self.editFunc)

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

    def getNode(self):
        global nodeID
        data = nodeCollection.find({'Client ID': nodeID})
        for x in data: pass
        self.alias = x['Alias']
        self.clientId = x['Client ID']

    def editFunc(self):
        global nodeID
        Alias = self.aliasInput.text()
        ClientID = self.clientInput.text()

        if Alias and ClientID != '':
            data = {'Alias': Alias, 'Client ID': ClientID}
            query = {'Client ID': nodeID}
            newValue = {'$set': data}
            nodeCollection.update_one(query, newValue)
            QMessageBox.information(self, 'SUCCESS', 'The Node has been updated')
            w.getNode()
        else:
            QMessageBox.information(self, 'WARNING', 'Fields can not be empty')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
