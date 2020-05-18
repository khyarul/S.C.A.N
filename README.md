# S.C.A.N
 Small and Cheap Attendance Node

# Attendance Node Machine
Hardware: ESP8266 Wemos D1 Mini - Software: Arduino C/C++

Feature and library used:
 - Dual Mode: Tap to Unlock Door and Attendance Mode
 - Scheduler.h (Multitask)
 - PubSubClient.h (MQTT protocol client)
 - LiquidCrystal_I2C.h (LCD16x2 I2C)
 - MFRC522.h (RFID SPI module 13.56MHz)
 - ArduinoOTA.h (wireless/no-usb programming)
 - Reed/magnetic sensor for Door state
 - solenoid door lock port max. 12V/1A (12W)
 - 5V/3A (15W) power supply input

# GUI (Node Monitor & Employee Manager)
Main file: **"SCAN_node_monitor.py"** (**"karyawan.py"**, **"icons"**, and **"images" need to be in the same folder**)

Feature:
 - Manage & monitor all Node Machine that connected to the same MQTT server.
 - Using MongoDB database for Node & Employee Manager.
 - Unlock door on every Node Machine remotely.

Python 3.7 module/library used:
 - Pyqt5 (for GUI)
 - PyMongo (for MongoDB Database driver)
 - Paho-Mqtt (MQTT client)
 - Threading (Multitasking using Multithreading, 1 thread per 1 Attendance Node Machine)

# Support & DONATE this open source project:
  - PAYPAL  : [SentinelCreative](https://www.paypal.me/sentinelcreative "PAYPAL")
  - BNI     : 0718053662 (Khyarul Arham)
  - Mandiri : 1130012279398 (Khyarul Arham)
