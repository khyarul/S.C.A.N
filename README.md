# S.C.A.N
 Small and Cheap Attendance Node

# Node Machine
Hardware: ESP8266 Wemos D1 Mini
Software: Arduino C/C++

Feature and library used:
 - Scheduler.h (Multitask)
 - PubSubClient.h (MQTT protocol client)
 - LiquidCrystal_I2C.h (LCD16x2 I2C)
 - MFRC522.h (RFID SPI module 13.56MHz)
 - ArduinoOTA.h (wireless/no-usb programming)
 - Reed/magnetic sensor for Door state
 - solenoid max. 12V/1A (12W) port
 - 5V/3A power supply input

# GUI
Main file: "SCAN_node_monitor.py" ("karyawan.py", "icons", and "images" need to be in the same folder)

Python external module/library used:
 - Python 3.7
 - Pyqt5 (for GUI)
 - PyMongo (for MongoDB Database driver)
 - Paho-Mqtt (MQTT client)
 - Threading (Multitasking using Multithreading, 1 thread per Node)

DONATE: 
  - PAYPAL  : [SentinelCreative](https://www.paypal.me/sentinelcreative "PAYPAL")
  - BNI     : 0718053662 (Khyarul Arham)
  - Mandiri : 1130012279398 (Khyarul Arham)
