/*
Nome: mqtt.ino
Data: 2018/11/22

Sensores utilizados 
  -> Luminosidade 
  -> Temperatura DHT11
  -> Umidade do solo 

Extensões de portas digitais 
  -> Conversor ads1115
*/



// NECESSÁRIOS PARA O PROJETO
#include <FS.h>                   //this needs to be first, or it all crashes and burns...
#include <ESP8266WiFi.h>          //https://github.com/esp8266/Arduino
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>          //https://github.com/tzapu/WiFiManager
#include <PubSubClient.h>
#include <ArduinoJson.h>          //https://github.com/bblanchon/ArduinoJson
#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>


// DEFINES DA VIDA!
#define luminosidade 2
#define umidade_solo 3
#define DHT_PORT D5
#define DHT_TYPE DHT11
#define ADS1 D1
#define ADS2 D2

//define your default values here, if there are different values in config.json, they are overwritten.
//length should be max size + 1 

// Variaveis essenciais 
char mqtt_server[40];
char mqtt_port[6];
char mqtt_user[20];
char mqtt_passwd[20];
char sensor_id[5];
char umid[26];
char temp[30];
char lum[31];
int16_t valor=0;




WiFiClient esp8266;
PubSubClient client(esp8266);
Adafruit_ADS1115 ads(0x48);  /* Usado por padrao no ads1115 */
DHT dht(DHT_PORT, DHT_TYPE);

void mqtt_callback(char* topic, byte* payload, unsigned int length)
{
  char rxj[512];
  for ( int i = 0; i < length; i++)
  {
    rxj[i] = payload[i];
  }
  Serial.println(rxj);
  }
  
//flag for saving data
bool shouldSaveConfig = false;
//boolean clean_g = false;
//callback notifying us of the need to save config

void saveConfigCallback () {
  Serial.println("Should save config");
  shouldSaveConfig = true;
}

void setup()
{
  Wire.begin(ADS2, ADS1);
  Serial.begin(115200);
  Serial.println();
  dht.begin();
  ads.begin();
  setup_wifi_mqtt();
}
  
  

void setup_wifi_mqtt() {
  // put your setup code here, to run once:

  //clean FS, for testing
  Serial.print("Formatando...");
  SPIFFS.format();
  Serial.print("Formatacao completa");
  
  //read configuration from FS json
  Serial.println("mounting FS...");


  // Aqui salva a porra no FLASH
  if (SPIFFS.begin()) {
    Serial.println("mounted file system");
    if (SPIFFS.exists("/config.json")) {
      //file exists, reading and loading
      Serial.println("reading config file");
      File configFile = SPIFFS.open("/config.json", "r");
      if (configFile) {
        Serial.println("opened config file");
        size_t size = configFile.size();
        // Allocate a buffer to store contents of the file.
        std::unique_ptr<char[]> buf(new char[size]);

        configFile.readBytes(buf.get(), size);
        DynamicJsonBuffer jsonBuffer;
        JsonObject& json = jsonBuffer.parseObject(buf.get());
        json.printTo(Serial);
        if (json.success()) {
          Serial.println("\nparsed json");

          strcpy(mqtt_server, json["mqtt_server"]);
          strcpy(mqtt_port, json["mqtt_port"]);
          strcpy(mqtt_user, json["mqtt_user"]);
          strcpy(mqtt_user, json["mqtt_passwd"]);
          //strcpy(blynk_token, json["blynk_token"]);
          strcpy(sensor_id, json["sensor_id"]);
          

          /*if(json["ip"]) {
            //Serial.println("setting custom ip from config");
            //static_ip = json["ip"];
            //strcpy(static_ip, json["ip"]);
            // strcpy(static_gw, json["gateway"]);
            //strcpy(static_sn, json["subnet"]);
            //strcat(static_ip, json["ip"]);
            //static_gw = json["gateway"];
            //static_sn = json["subnet"];
            //Serial.println(static_ip);
            Serial.println("converting ip");
            IPAddress ip = ipFromCharArray(static_ip);
            Serial.println(ip);
          } else {
              Serial.println("no custom ip in config");
          }
        } else {
         Serial.println("failed to load json config");
        }*/
      }
    }
  } else {
    Serial.println("failed to mount FS");
  }
  //end read
  //Serial.println(static_ip);
  //Serial.println(blynk_token);
  Serial.println(mqtt_server);
  Serial.println(sensor_id);


  // The extra parameters to be configured (can be either global or just in the setup)
  // After connecting, parameter.getValue() will get you the configured value
  // id/name placeholder/prompt default length
  WiFiManagerParameter custom_mqtt_server("server", "mqtt server", mqtt_server, 40);
  WiFiManagerParameter custom_mqtt_port("port", "mqtt port", mqtt_port, 5);
  WiFiManagerParameter custom_mqtt_user("user", "mqtt user", mqtt_user, 20);
  WiFiManagerParameter custom_mqtt_passwd("passwd", "mqtt passwd", mqtt_passwd, 20);
  //WiFiManagerParameter custom_blynk_token("blynk", "blynk token", blynk_token, 34);
  WiFiManagerParameter custom_sensor_id("Sensor_id", "Sensor ID", sensor_id, 5);
  

  //WiFiManager
  //Local intialization. Once its business is done, there is no need to keep it around
  WiFiManager wifiManager;

  
  //set config save notify callback
  wifiManager.setSaveConfigCallback(saveConfigCallback);

  //set static ip
  //IPAddress _ip,_gw,_sn;
  //_ip.fromString(static_ip);
  //_gw.fromString(static_gw);
  //_sn.fromString(static_sn);

  // wifiManager.setSTAStaticIPConfig(_ip, _gw, _sn); //IP STATIC
  
  //add all your parameters here
  wifiManager.addParameter(&custom_mqtt_server);
  wifiManager.addParameter(&custom_mqtt_port);
  wifiManager.addParameter(&custom_mqtt_user);
  wifiManager.addParameter(&custom_mqtt_passwd);
  //wifiManager.addParameter(&custom_blynk_token);
  wifiManager.addParameter(&custom_sensor_id);
  //reset settings - for testing
  wifiManager.resetSettings();

  //set minimu quality of signal so it ignores AP's under that quality
  //defaults to 8%
  wifiManager.setMinimumSignalQuality();
  
  //sets timeout until configuration portal gets turned off
  //useful to make it all retry or go to sleep
  //in seconds
  //wifiManager.setTimeout(120);

  //fetches ssid and pass and tries to connect
  //if it does not connect it starts an access point with the specified name
  //here  "AutoConnectAP"
  //and goes into a blocking loop awaiting configuration
  if (!wifiManager.autoConnect("GardenLife", "tccredes")) {
    Serial.println("Falha na conexao");
    delay(3000);
    //reset and try again, or maybe put it to deep sleep
    ESP.reset();
    delay(5000);
  }

  //if you get here you have connected to the WiFi
  Serial.println("connected...yeey :)");

  //read updated parameters
  strcpy(mqtt_server, custom_mqtt_server.getValue());
  strcpy(mqtt_port, custom_mqtt_port.getValue());
  strcpy(mqtt_user, custom_mqtt_user.getValue());
  strcpy(mqtt_passwd, custom_mqtt_passwd.getValue());
  //strcpy(blynk_token, custom_blynk_token.getValue());
  strcpy(sensor_id, custom_sensor_id.getValue());

  //save the custom parameters to FS
  if (shouldSaveConfig) {
    Serial.println("saving config");
    DynamicJsonBuffer jsonBuffer;
    JsonObject& json = jsonBuffer.createObject();
    json["mqtt_server"] = mqtt_server;
    json["mqtt_port"] = mqtt_port;
    json["mqtt_user"] = mqtt_user;
    json["mqtt_passwd"] = mqtt_passwd;
    json["sensor_id"] = sensor_id;
    //json["blynk_token"] = blynk_token;

    json["ip"] = WiFi.localIP().toString();
    json["gateway"] = WiFi.gatewayIP().toString();
    json["subnet"] = WiFi.subnetMask().toString();

    File configFile = SPIFFS.open("/config.json", "w");
    if (!configFile) {
      Serial.println("failed to open config file for writing");
    }

    json.prettyPrintTo(Serial);
    json.printTo(configFile);
    configFile.close();
    //end save
  }
  Serial.println("IP LOCAL:");
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.gatewayIP());
  Serial.println(WiFi.subnetMask());

  // MQTT SERVER
  client.setServer(mqtt_server, atoi(mqtt_port));
  client.setCallback(mqtt_callback);
  if (client.connect(sensor_id, mqtt_user, mqtt_passwd))
  {
    Serial.println("Conectado ao Broker com Sucesso ^^");
    Serial.println("Inserindo valor teste");    
    snprintf(temp, 30, "/home/horta/id_%s/temperatura", sensor_id ); // temperatura
    snprintf(umid, 26, "/home/horta/id_%s/umidade", sensor_id ); // umidade
    snprintf(lum, 31, "/home/horta/id_%s/luminosidade", sensor_id ); // luminosidade
    client.publish( temp , "123");
  }
  }
}

void reconnect() {
  // Recconect Loop
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (client.connect(sensor_id, mqtt_user, mqtt_passwd)) {
      Serial.println("[STATUS] connected :)");
    } else {
      Serial.println("[STATUS] Failed :(");
      Serial.println("RESPOSTA:");
      Serial.println(client.state());
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


// Esta no conversor 
void luminosidade_sensor()
{
  /*
   * < 500 = Claro
   * > 500 = Escuro
   */
  valor = ads.readADC_SingleEnded(luminosidade); // luminosidade 2
  valor=map(valor, 0,20000, 100, 0);
  //Porcentagem do sensor
  client.publish(lum, String(valor).c_str());
  Serial.print("Luminosidade: "); Serial.print(valor);
}

// Esta no conversor 
void umidade_sensor()
{
   /* 
    *  > 0 e < 400 = umido 
    *  > 400 e < 800 = moderado
    *  > 800 e < 1024 = seco
    */
   valor = ads.readADC_SingleEnded(umidade_solo); // umidade 3
   // Porcentagem do sensor
   valor=map(valor, 0,20000, 100, 0); // Porcentagem 
   client.publish(umid, String(valor).c_str());
   Serial.print("Umidade: "); Serial.print(valor); 
}


void temperatura()
{
  /*
  Sensor DHT11 
  Nota: Usado em Graus Celsius
  */
  
  valor = dht.readTemperature();
  client.publish(temp, String(valor).c_str());
  Serial.print("Temperatura: "); Serial.print(valor); 
}


void loop() {
  // put your main code here, to run repeatedly:
  if (!client.connected())
  {
      reconnect();  
  }
  client.loop();
  umidade_sensor();
  luminosidade_sensor();
  temperatura();
  delay(10000);
  
}
