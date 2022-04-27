#include <WiFi.h>
#include "time.h"
#include  <ArduinoJson.h>
#include "HTTPClient.h"

//==================Global variables======================
const char *wifi_ssid = "xxxxxxxxx";      // your network SSID (name)
const char *wifi_pass = "xxxxxxxxx";   // your network password
String SensorReading;
String cse_ip = "x.x.x.x";        // YOUR IP from ipconfig/ifconfig
String cse_port = "8080";
String server = "http://" + cse_ip + ":" + cse_port + "/~/in-cse/in-name/";
String ae = "Readings";
String cnt1 = "Current_rpm";
String cnt2 = "Average_rpm";
String cnt3 = "Session_time";
String cnt4 = "Distance";
String cnt5 = "Start_flag";
String cnt6 = "Session_id";


//=============== Defined values ================
#define wheelsize 26
#define pi 3.1416
#define TOT 20
#define THRESHOLD -3
#define BASE -1
#define G  4
int gears[] = {21,19,18,5};
int touchThreshold = 20;
int cadence_gears[] = {20, 40, 70};

//============== Pins ===========================
#define LedStart 2
#define touchPin 4

//=============== reqd =========================
int tvalue_on, tvalue_off;
int arr[TOT];
int x =0;
float val = 0;
int Session_id=1;

//=============== Outputs =======================
int rotation = 0;
double rpm=0, dist =0;
unsigned long r_time=0;
double currentRPM =0;
int prev =0;
unsigned long StartTime = 0;
unsigned long EndTime =0;
unsigned long RotStartTime = 0;
unsigned long RotEndTime =0;
double SessionTime =0;

//=============== Functions ====================
void ConnectToWifi()
{
  while (WiFi.status() != WL_CONNECTED) {
    
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(wifi_ssid);
    WiFi.begin(wifi_ssid, wifi_pass);
    // wait 10 seconds for connection:
    delay(10000);
  }
  Serial.print("Connected to the network with ip:");
  Serial.println(WiFi.localIP());
}

void CreateContentInstance(String val, String container)
{
  // Serial.print("<<<<<<<<<<<<<<<<<<<<<<<<<<<");
  // Serial.println(container);
  HTTPClient http;
  http.begin(server + ae + "/" + container + "/");
  http.addHeader("X-M2M-Origin", "admin:admin");
  http.addHeader("Content-Type", "application/json;ty=4");
  int code = http.POST("{\"m2m:cin\": {\"cnf\":\"application/json\",\"con\": " + String(val) + "}}");
  // Serial.println(code); // To debug
  if (code == -1) {
    Serial.println("UNABLE TO CONNECT TO THE SERVER");
  }
  http.end();
}

void reset(){
  for (int i=0; i<TOT; i++)
    arr[i] = hallRead();
}

float mean(){
  int m = 0;
  for (int i=0; i<TOT; i++)
    m+=arr[i];
  return (float)m/TOT;
}

double CalcCurrentRPM(unsigned long stime)// stime is in milli seconds
{
  double r = 60000/stime;
  return r;
}


unsigned long UpdatCandence(){
  int retval;
  while(touchRead(T3) > touchThreshold){
    arr[x++ % TOT] = hallRead();
    val = mean();
    if (val < THRESHOLD){
      Serial.print(val);
      while(mean() < BASE){
        if (touchRead(T3) < touchThreshold){
          return -1;
        }
        reset();
      }
      RotEndTime = millis();
      retval = RotEndTime - RotStartTime;
      Serial.print(": ");
      Serial.println(retval);
      return retval;
    }
  }
  return -1;
}

int distance(){ // Distance Function
  return (2*pi*wheelsize*rotation); 
}


int gearCheck(){ //gear
  int i;
  for (i=0; i<G-1 ;i++){
    if (currentRPM < cadence_gears[i])
    {
       break;
    }
  }
  return i;
}

//================Main============================
void setup() {
  Serial.begin(115200);
  pinMode(LedStart, OUTPUT);
  for (int i =0 ; i<G; i++){
    pinMode(gears[i], OUTPUT);
    digitalWrite(gears[i], LOW);
  }
  digitalWrite(LedStart, LOW);
  reset();
  ConnectToWifi();
}

void loop() {
  digitalWrite(LedStart, LOW);
  tvalue_on = touchRead(T0); // T0 corressponds GPIO 4
  Serial.println("On Touch: ");
  Serial.println(tvalue_on);
  if(tvalue_on < touchThreshold) 
  {
    StartTime = millis();
    RotStartTime = millis();
    Serial.println("Session Started");
    digitalWrite(LedStart, HIGH);
    CreateContentInstance(String(1), cnt5);
    //CreateContentInstance(String(Session_id), cnt6);  
    Serial.println("here------------------------\n");
    while(touchRead(T3) > touchThreshold)
      {
        r_time = UpdatCandence();
        // Calculating required values
        if(r_time == -1)
        {
          break;
        }
        currentRPM = CalcCurrentRPM(r_time);
        if (currentRPM > 100) continue;
        rotation++;
        CreateContentInstance(String(currentRPM), cnt1);
        CreateContentInstance(String(Session_id), cnt6); 
        digitalWrite(gears[prev], LOW);
        prev = gearCheck();
        digitalWrite(gears[prev], HIGH);
        Serial.print("r_time: ");
        Serial.println(r_time);
        Serial.print("currentRPM: ");
        Serial.println(currentRPM);
        Serial.println("------------------");
        RotStartTime = millis();
      }
      
      digitalWrite(gears[prev], LOW);
      Serial.println("\nSession Finished");
      CreateContentInstance(String(0), cnt5);
      EndTime =millis();
      
      
      // Calculating required values
      SessionTime =(EndTime -StartTime)/1000;
      rpm =(rotation/SessionTime)*60;
      dist = (double)distance()/12;
      // printing
      Serial.print(">>>>>>>>>>> avg cadence: ");
      Serial.print(rpm);
      Serial.println(" rpm");
      Serial.print(">>>>>>>>>>> distance travelled in session: ");
      Serial.print(dist);
      Serial.println(" ft");
      // Posting those values
      CreateContentInstance(String(SessionTime), cnt3);
      CreateContentInstance(String(rpm), cnt2);
      CreateContentInstance(String(dist), cnt4);
      
      //digitalWrite(gears[gearCheck()], HIGH);
      rotation = 0;
      rpm =0;
      StartTime =0;
      EndTime =0;
      RotStartTime =0;
      RotEndTime =0;
      SessionTime =0;
      Session_id++;
  }
  delay(1000);
}
