#include <LiquidCrystal.h>

String str;
LiquidCrystal lcd (8, 9, 4, 5, 6, 7);

void printToLcd(String str) {
  lcd.clear();
  int bufSize = 33;
  char buf[bufSize];
  for(int i = 0; i < bufSize; i++) {
    buf[i] = ' ';
  }
  str.toCharArray(buf, bufSize);
  int k = 0;
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 16; j++) {
      lcd.setCursor(j, i);
      //Serial.println(ch);
      lcd.write(buf[k]);
      k++;
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  str = "";
  lcd.begin(16, 2);
  Serial.begin(9600);
  Serial.print("ready");
  //String initStr = "0123456789ABCDEF0123456789ABCDEF";
  //printToLcd(initStr);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    str = Serial.readStringUntil('\n');
    //str = Serial.readString();
    //Serial.read();
    printToLcd(str);
    Serial.println(str);
    printToLcd(str);
  }
  delay(10);
}
