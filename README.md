# S.C.A.N
 Small and Cheap Attendance Node

## Attendance Node Machine
   - Hardware: ESP8266 Wemos D1 Mini - Software: Arduino C/C++

   - Feature and library used:
     - [x] Dual Mode: Tap to Unlock Door and Attendance Mode
     - [x] Scheduler.h (Multitask) from [Here](https://github.com/nrwiersma/ESP8266Scheduler)
     - [x] PubSubClient.h (MQTT protocol client)
     - [x] LiquidCrystal_I2C.h (LCD16x2 I2C)
     - [x] MFRC522.h (RFID SPI module 13.56MHz)
     - [x] ArduinoOTA.h (wireless/no-usb programming)
     - [x] Reed/magnetic sensor for Door state
     - [x] solenoid door lock port max. 12V/1A (12W)
     - [x] 5V/3A (15W) power supply input
   
   - Recommended ESP8266 Wemos D1 Mini Arduino Configuration:
   
   ![arduino config](https://user-images.githubusercontent.com/50608159/82400250-0d21d080-9a81-11ea-8ff0-8537a739b395.png)
   
   - Mechanic Documentation Photo:
     - **Acrylic Case for LCD, RFID sensor, button, and buzzer. Install it outside the room.**
![img](https://i.ibb.co/nwVVGG5/IMG-20200515-223923.jpg)
![img](https://i.ibb.co/mNFmP1P/IMG-20200515-223940.jpg)
![img](https://i.ibb.co/tsFh6h2/IMG-20200515-223957.jpg)
     - **Acrylic case for controller part, reed/magnet sensor and solenoid port. Install it inside the room.**
![img](https://i.ibb.co/6RDryc6/IMG-20200515-224018.jpg)
![img](https://i.ibb.co/F5jDfyX/IMG-20200515-224027.jpg)
     - **Solenoid port and small hole for reed/magnet sensor wire**
![img](https://i.ibb.co/JRx0fvC/IMG-20200515-224034.jpg)
![img](https://i.ibb.co/M5sH3cK/IMG-20200515-224110.jpg)
![img](https://i.ibb.co/rQfbF8Z/IMG-20200515-224124.jpg)
   
## GUI (Node Monitor & Employee Manager)
- Main file: **"SCAN_node_monitor.py"** (**"karyawan.py"**, **"icons"**, and **"images" need to be in the same folder**)

- Feature:
  - [x] Manage & monitor all Node Machine that connected to the same MQTT server.
  - [x] Using MongoDB database for Node & Employee Manager.
  - [x] Unlock door on every Node Machine remotely.

- Python 3.7 module/library used:
  - [x] Pyqt5 (for GUI)
  - [x] PyMongo (for MongoDB Database driver)
  - [x] Paho-Mqtt (MQTT client)
  - [x] Threading (Multitasking using Multithreading, 1 thread per 1 Attendance Node Machine)

## Support & DONATE this open source project:
  - PAYPAL  : [SentinelCreative](https://www.paypal.me/sentinelcreative "PAYPAL")
  - BNI     : 0718053662 (Khyarul Arham)
  - Mandiri : 1130012279398 (Khyarul Arham)
