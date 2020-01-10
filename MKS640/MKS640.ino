#include "CommandHandler.h"
#include <Wire.h>

#define MCP4725_ADDR 0x60

CommandHandler<> SerialCommandHandler;

const int ValveTestPoint = 10; // D10 read
const int PressureSigOutput = 1; // A0 read
const int ValveClose = 8; // D8 write
const int ValveOpen = 9; // D9 write
const int TripPointA = 11; // D11 read
const int TripPointB = 12; // D12 read
const int ledPin = 13; // D13 write

int stat;
int pressure;

void setup() {
  Wire.begin();
  
  Serial.begin(9600);
  SerialCommandHandler.AddCommand(F("SP"), Cmd_SetPressure);
  SerialCommandHandler.AddCommand(F("GP"), Cmd_GetPressure);
  SerialCommandHandler.AddCommand(F("CP"), Cmd_ControlPressure);
  SerialCommandHandler.AddCommand(F("OV"), Cmd_OpenValve);
  SerialCommandHandler.AddCommand(F("CV"), Cmd_CloseValve);
  SerialCommandHandler.AddCommand(F("TV"), Cmd_TestValve);
  SerialCommandHandler.AddCommand(F("TPA"), Cmd_TripPointA);
  SerialCommandHandler.AddCommand(F("TPB"), Cmd_TripPointB);
  SerialCommandHandler.SetDefaultHandler(Cmd_Unknown);

  pinMode(ValveTestPoint, INPUT);
  pinMode(ValveClose, OUTPUT);
  pinMode(ValveOpen, OUTPUT);
  pinMode(TripPointA, INPUT);
  pinMode(TripPointB, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  SerialCommandHandler.Process();
}

void Cmd_SetPressure(CommandParameter &Parameters) {
  pressure = Parameters.NextParameterAsInteger(pressure);
  Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(64);
  Wire.write(pressure >> 4);
  Wire.write((pressure & 15) << 4);
  Wire.endTransmission();
  Serial.print("SP=");
  Serial.println(pressure);
}

void Cmd_GetPressure() {
  pressure = analogRead(PressureSigOutput);
  Serial.print("GP=");
  Serial.println(pressure);
}

void Cmd_ControlPressure() {
  digitalWrite(ValveClose, HIGH);
  digitalWrite(ValveOpen, HIGH);
  Serial.println("PC");
}

void Cmd_OpenValve() {
  digitalWrite(ValveClose, HIGH);
  digitalWrite(ValveOpen, LOW);
  digitalWrite(ledPin, HIGH);
  Serial.println("VO");
}

void Cmd_CloseValve() {
  digitalWrite(ValveOpen, HIGH);
  digitalWrite(ValveClose, LOW);
  digitalWrite(ledPin, LOW);
  Serial.println("VC");
}

void Cmd_TestValve() {
  stat = digitalRead(ValveTestPoint);
  Serial.print("TV=");
  Serial.println(stat);
}

void Cmd_TripPointA() {
  stat = digitalRead(TripPointA);
  Serial.print("TPA=");
  Serial.println(stat);
}

void Cmd_TripPointB() {
  stat = digitalRead(TripPointB);
  Serial.print("TPB=");
  Serial.println(stat);
}

void Cmd_Unknown() {
  Serial.println("ER");
}
