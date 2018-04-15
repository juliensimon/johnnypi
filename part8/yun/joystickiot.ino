#include <aws_iot_mqtt.h>
#include <aws_iot_version.h>
#include "aws_iot_config.h"

// Analog pins for x, y and switch
const int pinX  = 0;
const int pinY  = 1;

int calX, calY, rawX, rawY;

aws_iot_mqtt_client myClient;
char msg[64];
int rc;

void setup() {
  
  SerialUSB.begin(115200);  // initialize serial communication
  while (!SerialUSB);       // do nothing until the serial monitor is opened

  // Calibrate x, y and switch
  calX  = analogRead(pinX);
  calY  = analogRead(pinY);

  // Connect to the IoT Gateway
  sprintf(msg, "AWS IoT SDK Version(dev) %d.%d.%d-%s\n", VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, VERSION_TAG);
  Serial.println(msg);
  if ((rc = myClient.setup(AWS_IOT_CLIENT_ID)) == 0) {
    if ((rc = myClient.config(AWS_IOT_MQTT_HOST, AWS_IOT_MQTT_PORT, AWS_IOT_ROOT_CA_PATH, AWS_IOT_PRIVATE_KEY_PATH, AWS_IOT_CERTIFICATE_PATH)) == 0) {
      if ((rc = myClient.connect()) == 0) {
        sprintf(msg, "Connected");
      }
      else {
        sprintf(msg, "Connect failed, error=%d", rc);
      }
    }
    else {
      sprintf(msg, "Config failed, error=%d", rc);
    }
  }
  else {
    sprintf(msg, "Setup failed, error=%d", rc);
  }
  Serial.println(msg);

  
  // Delay to make sure SUBACK is received, delay time could vary according to the server
  delay(2000);
}

void loop() {
  // Read values for x, y and switch
  rawX  = analogRead(pinX)  - calX;
  rawY  = analogRead(pinY)  - calY;

  if (rawX > 200) {
    sprintf(msg, "left");
  }
  else if (rawX < -200) {
    sprintf(msg, "right");
  }
  else if (rawY > 200) {
    sprintf(msg, "forward");
  }
  else if (rawY < -200) {
    sprintf(msg, "backward");
  }
  else {
    sprintf(msg, "stop");
  }
  
  // Publish to JohnnyPi/move with reliable delivery (QoS=1)
  if ((rc = myClient.publish("JohnnyPi/move", msg, strlen(msg), 1, false)) != 0) {
    sprintf(msg, "Publish to JohnnyPi/move failed, error=%d", rc);
  }
  Serial.println(msg);

  delay(1000);
}
