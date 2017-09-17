
#ifndef config_usr_h
#define config_usr_h

// Copy and paste your configuration into this file
//===============================================================
#define AWS_IOT_MQTT_HOST "XXX.iot.eu-west-1.amazonaws.com"
// your endpoint
#define AWS_IOT_MQTT_PORT 8883
// your port
#define AWS_IOT_CLIENT_ID      "Yun"
// your client ID
#define AWS_IOT_MY_THING_NAME "Yun"
// your thing name
#define AWS_IOT_ROOT_CA_FILENAME "root-CA.crt"
// your root-CA filename
#define AWS_IOT_CERTIFICATE_FILENAME "XXX-certificate.pem.crt"
// your certificate filename
#define AWS_IOT_PRIVATE_KEY_FILENAME "XXX-private.pem.key"
// your private key filename
//===============================================================

// SDK config, DO NOT modify it
#define AWS_IOT_PATH_PREFIX "/root/AWS-IoT-Python-Runtime/certs/"
#define AWS_IOT_ROOT_CA_PATH AWS_IOT_PATH_PREFIX AWS_IOT_ROOT_CA_FILENAME		// use this in config call
#define AWS_IOT_CERTIFICATE_PATH AWS_IOT_PATH_PREFIX AWS_IOT_CERTIFICATE_FILENAME	// use this in config call
#define AWS_IOT_PRIVATE_KEY_PATH AWS_IOT_PATH_PREFIX AWS_IOT_PRIVATE_KEY_FILENAME	// use this in config call

#endif
