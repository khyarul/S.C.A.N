# S.C.A.N
 Small and Cheap Attendance Node

## Attendance Node Machine
   - Hardware: ESP8266 Wemos D1 Mini - Software: Arduino C/C++

   - Feature and library used:
     - [x] Dual Mode: **Tap to Unlock Door** and **Attendance Mode**
     - [x] Scheduler.h (Multitask) from [Here](https://github.com/nrwiersma/ESP8266Scheduler)
     - [x] PubSubClient.h (MQTT protocol client)
     - [x] LiquidCrystal_I2C.h (LCD16x2 I2C)
     - [x] MFRC522.h (RFID SPI module 13.56MHz)
     - [x] ArduinoOTA.h (wireless/no-usb programming)
     - [x] Reed/magnetic sensor for Door state
     - [x] solenoid door lock port max. 12V/1A (12W)
     - [x] 5V/3A (15W) power supply input
   
   - Recommended ESP8266 Wemos D1 Mini Arduino Configuration:
   
   ![arduino config](https://user-images.githubusercontent.com/50608159/88420036-6b1bbd00-ce10-11ea-89b4-321394aa3499.png)
 
   - Wemos D1 Mini Port Allocation:
   
 PORT |	FUNCTION |	DEVICE
 -----|----------|-------   
 D1 |	I2C SCL |	LCD 16x2
 D2 |	I2C SDA |	LCD 16x2
 D4 |	SPI Reset |	RC522
 D5 |	SPI SCK |	RC522
 D6 |	SPI MISO |	RC522
 D7 |	SPI MOSI	| RC522
 D8 |	SPI SS	| RC522
 D0 |	Digital Output	| Solenoid
 TX |	Digital Input	| Attendance Mode button
 RX |	Digital Output |	Buzzer
 D3 |	Digital Input |	“Unlock Door” Mode button
 A0 |	Analog Input |	Magnetic Switch/Sensor

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
- Tested on Windows 10 PC and Ubuntu Mate 18.04 64bit on Raspberry Pi 3 (Should be supported with Ubuntu 64bit on PC)
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
  - BNI     : 1284959883 (Khyarul Arham)
  - Jago    : 504120557241 (Khyarul Arham)
