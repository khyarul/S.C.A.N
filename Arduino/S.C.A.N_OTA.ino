/*
   MQTT Small & Cheap Attendance Node (S.C.A.N) V1.0
   Programmed by Khyarul Arham - Sentinel
*/
#include <Scheduler.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN D8
#define RST_PIN D4

LiquidCrystal_I2C lcd(0x3F, 16, 2);		//use 0x27 if you have different lcd i2c address
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;

const char* ssid PROGMEM = "SSID name"; //WiFi Host
const char* pass PROGMEM = "WiFi Password";          //WiFi pass

const char* broker PROGMEM = "MQTT host/server";    //mqtt host
const int16_t port PROGMEM = 1883;                //mqtt port
const char* clientID PROGMEM = "Client ID";          //mqtt client ID, don't use character: " - "
const char* host PROGMEM = "OTA host name";      //OTA host name, bebas
const char* username PROGMEM = "MQTT username";        //mqtt username
const char* password PROGMEM = "MQTT password";         //mqtt pass

int8_t BUZZER = 0, preButton = 1, doorButton = 1, SCREEN = 1, MODE = 0;
uint8_t screenTimer = 10;   //Screen will turn OFF after x seconds idle (default 10s)

WiFiClient wemos;
PubSubClient mqtt;

#define lock_ON digitalWrite(D0, 0)
#define lock_OFF digitalWrite(D0, 1)
String RESPON = "", TIME = "-No Time Update-", LOCK = "1";
//char TOPIC[16] = "";
char responTopic[16] = "RESPON/";
char uidTopic[16] = "UID/";
char statusTopic[16] = "STATUS/";
char lockTopic[16] = "LOCK/";     //remote button topic
char doorTopic[16] = "DOOR/";
//=========================Scheduler================================
//==================================================================
class mainLoop : public Task {
  public:
    void loop() {
mulai:
      lcd.setCursor(0, 0); lcd.print(TIME);
      //      char reedBuff[16];
      //      sprintf(reedBuff, "%4d", reed);
      //      lcd.setCursor(0,0); lcd.print(reedBuff);
      if (preButton == 0) {
        SCREEN = 1;
        MODE = 1;
      }
      else if (doorButton == 0) {
        SCREEN = 1;
        MODE = 0;
      }
      if (MODE == 0) {
        lcd.setCursor(0, 1); lcd.print(F(" TAP TO UNLOCK "));
      }
      else {
        lcd.setCursor(0, 1); lcd.print(F("ATTENDANCE MODE"));
      }
      yield();
      // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle. And if present, select one.
      if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        goto mulai;
      }

      SCREEN = 1;
      MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      String idStr = "";
      char id[16] = "";
      for (uint8_t i = 0; i < rfid.uid.size; i++) {
        idStr += String(rfid.uid.uidByte[i], HEX);
      }
      idStr.toUpperCase();
      if (MODE == 0) {
        idStr = "0:" + idStr;
      }
      else {
        idStr = "1:" + idStr;
      }
      lcd.clear();
      lcd.setCursor(0, 0); lcd.print(F("Checking..."));
      //      lcd.setCursor(0, 0); lcd.print(rfid.PICC_GetTypeName(piccType));
      //      lcd.setCursor(0, 1); lcd.print(idStr);
      strcpy_P(id, idStr.c_str());
      mqtt.publish(uidTopic, id);

      while (1) {
        if (RESPON == "") {
        }
        else if (RESPON == "0") {
          BUZZER = 2;
          lcd.clear();
          lcd.setCursor(0, 0); lcd.print(F("    Sorry :(   "));
          lcd.setCursor(0, 1); lcd.print(F("UNREGISTERED ID"));
          break;
        }
        else {
          BUZZER = 1;
          if (MODE == 0) {
            LOCK = "0";
          }
          lcd.clear();
          lcd.setCursor(0, 0); lcd.print(F("SUCCESS, WELCOME"));
          lcd.setCursor(0, 1); lcd.print(RESPON);
          break;
        }
        yield();
      }
      RESPON = "";
      MODE = 0;
      rfid.PICC_HaltA();        // Halt PICC
      rfid.PCD_StopCrypto1();   // Stop encryption on PCD
      delay(2000);
      lcd.clear();
      //lcd.noBacklight();
    }
} main_loop;
//==================================================================
class mqttLoop : public Task {
  public:
    void loop() {
      if (!mqtt.connected()) {
        mqtt.connect(clientID, username, password, statusTopic, 2, 0, "0");
        mqtt.publish(statusTopic, "1"); //1=CONNECT, 0=DISCONNECT
        mqtt.subscribe(responTopic);
        mqtt.subscribe("PING");
        mqtt.subscribe("TIME");
        mqtt.subscribe(lockTopic);
      }
      mqtt.loop();
      delay(20);
    }
} mqtt_loop;
//==================================================================
//======================Button and Door Sensor======================
class buttonLoop : public Task {
  public:
    uint16_t reed;
    bool door = 0, doorState = 0;
    void setup() {
      //read Door Sensor on startup
      readDoor();
      if (door == 0) {
        mqtt.publish(doorTopic, "0");
      }
      else{
        mqtt.publish(doorTopic, "1");
      }
    }
    //===========
    void loop() {
      preButton = digitalRead(TX);
      doorButton = digitalRead(D3);
      //Baca & kirim status pintu saat berubah dari kondisi sebelumnya
      readDoor();
      if (doorState != door) {
        char buff[2];
        sprintf(buff, "%d", door);
        mqtt.publish(doorTopic, buff);
        doorState = door;
      }
      delay(50);
    }
    //Baca Sensor Reed/Magnet
    void readDoor() {
      reed = analogRead(A0);
      if (reed < 512) {
        door = 0;
      }
      else {
        door = 1;
      }
    }
} button_loop;
//==================================================================
class solenoidLoop : public Task {
  public:
    void loop() {
      if (LOCK == "0") {  //kunci OFF, buka kunci, solenoid ON
        lock_OFF;
        BUZZER = 1;
        delay(5000);
        lock_ON;
        delay(200);
      }
      else {              //kunci ON, solenoid OFF
        lock_ON;
      }
      LOCK = "";
      delay(50);
    }
} solenoid_loop;
//==================================================================
class buzzerLoop : public Task {
  public:
    void loop() {
      if (BUZZER == 1) {
        digitalWrite(RX, 1);
        delay(100);
        digitalWrite(RX, 0);
        delay(100);
        digitalWrite(RX, 1);
        delay(100);
        digitalWrite(RX, 0);
        BUZZER = 0;
      }
      else if (BUZZER == 2) {
        digitalWrite(RX, 1);
        delay(700);
        digitalWrite(RX, 0);
        BUZZER = 0;
      }
      else {
        digitalWrite(RX, 0);
      }
      delay(50);
    }
} buzzer_loop;
//==================================================================
class otaLoop : public Task {
  public:
    void loop() {
      ArduinoOTA.handle();
      delay(20);
    }
} ota_loop;
//==================================================================
class screenLoop : public Task {
  public:
    void loop() {
      if (SCREEN == 1) {
        SCREEN = 0;
        lcd.backlight();
        uint32_t now = millis();
        while ((millis() - now) < (screenTimer * 1000)) {
          if (SCREEN == 1) {
            SCREEN = 0;
            lcd.backlight();
            now = millis();
          }
          yield();
        }
        lcd.noBacklight();
      }
      else {
        lcd.noBacklight();
      }
    }
} screen_loop;
//==================================================================
//==================================================================

void setup() {
  pinMode(D0, OUTPUT);
  lock_ON;
  pinMode(D3, INPUT_PULLUP);
  pinMode(TX, INPUT_PULLUP);
  pinMode(RX, OUTPUT);

  lcd.begin();
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print(" Connecting...  ");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
  }

  ArduinoOTA.setHostname(host);
  ArduinoOTA.setPasswordHash("abef7bb1485a0a3d338debe3b1715fe8");
  ArduinoOTA.onStart([]() {});
  ArduinoOTA.onEnd([]() {});
  ArduinoOTA.onError([](ota_error_t error) {
    (void)error;
    ESP.restart();
  });
  ArduinoOTA.begin();

  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
  rfid.PCD_SetAntennaGain(rfid.RxGain_max);

  strcat_P(responTopic, clientID);
  strcat_P(uidTopic, clientID);
  strcat_P(statusTopic, clientID);
  strcat_P(lockTopic, clientID);
  strcat_P(doorTopic, clientID);
  mqtt.setClient(wemos);
  mqtt.setServer(broker, port);
  mqtt.connect(clientID, username, password, statusTopic, 2, 0, "0");   //broker akan mengirim will message "0" (disconnect) ke client lain yg subscribe ke topic ini jika node ini disconnect
  mqtt.setCallback(callback);
  mqtt.publish(statusTopic, "1"); //kirim status "1"=CONNECT
  mqtt.subscribe(responTopic);
  mqtt.subscribe("PING");
  mqtt.subscribe("TIME");
  mqtt.subscribe(lockTopic);

  lcd.clear();
  //lcd.noBacklight();

  Scheduler.start(&ota_loop);
  Scheduler.start(&mqtt_loop);
  Scheduler.start(&main_loop);
  Scheduler.start(&button_loop);
  Scheduler.start(&solenoid_loop);
  Scheduler.start(&buzzer_loop);
  Scheduler.start(&screen_loop);
  SCREEN = 1;
  BUZZER = 1;
  Scheduler.begin();
}

void loop() {}

void callback(char* topic, byte* payload, uint16_t len) {
  String payloadStr = "";
  for (uint16_t i = 0; i < len; i++) {
    payloadStr += char(payload[i]);
  }
  //int value = payloadStr.toInt();
  if (strcmp_P(topic, responTopic) == 0) {  //jika dapat message di responTopic
    //strcpy_P(TOPIC, topic);
    RESPON = payloadStr;
  }
  if (strcmp_P(topic, "PING") == 0 && payloadStr == "ping") { //jika dapat message "ping" di topic "PING"
    mqtt.publish(statusTopic, "1"); //kirim status "1"=CONNECT
  }
  if (strcmp_P(topic, "TIME") == 0) {   //jika dapat message di topic "TIME"
    TIME = payloadStr;  //update waktu
  }
  if (strcmp_P(topic, lockTopic) == 0) {    //remote button/topic utk kontrol solenoid
    LOCK = payloadStr;
    SCREEN = 1;
  }
}
