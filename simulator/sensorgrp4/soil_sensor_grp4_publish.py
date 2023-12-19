import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import random
import datetime
import sched
import sqlite3
from config import *
import requests


# Define ENDPOINT, TOPIC, RELATOVE DIRECTORY for CERTIFICATE AND KEYS
TOPIC = "iot/agritech"

# AWS class to create number of objects (devices)
class AWS():
    # Constructor that accepts client id that works as device id and file names for different devices
    # This method will obviosuly be called while creating the instance
    # It will create the MQTT client for AWS using the credentials
    # Connect operation will make sure that connection is established between the device and AWS MQTT
    def __init__(self, client, certificate, private_key):
        self.client_id = client
        self.device_id = client
        self.cert_path = certificate
        self.pvt_key_path = private_key
        #self.root_path = PATH_TO_CA
        self.myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(self.client_id)
        self.myAWSIoTMQTTClient.configureEndpoint(MQTT_ENDPOINT, 8883)
        self.myAWSIoTMQTTClient.configureCredentials("AmazonRootCA1.pem", self.pvt_key_path, self.cert_path)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        self._connect()
        self._openSensorConfigDb()
        self.msg_publish_loop_cntr = 0
        self._sensor_control_id = 0

    # Connect method to establish connection with AWS IoT core MQTT
    def _connect(self):
        self.myAWSIoTMQTTClient.connect()

    def _openSensorConfigDb(self):
        conn = sqlite3.connect('..//config.db')
        print("Opened Senor config database successfully");

        # create cursor object
        self.cur = conn.cursor()

    def _getSenorControlId(self):

        select_query = "SELECT ID, CONTROLID FROM SENSOR_CONFIG WHERE ID = '" + self.client_id + "';"""
        self.cur.execute(select_query)
        records = self.cur.fetchall()

        for row in records:
            print("Id: ", row[0])
            print("Anomaly State: ", row[1])

        return row[1]

    def _getActuatorStat(self):

        select_query = "SELECT ID, ACTUATORSTAT FROM SENSOR_CONFIG WHERE ID = '" + self.client_id + "';"""
        self.cur.execute(select_query)
        records = self.cur.fetchall()

        for row in records:
            print("Id: ", row[0])
            print("Actuator Status: ", row[1])

        return row[1]

        # This function gets the latitude, longitude and place values of sensor from sensor group config db

    def _getlocation(self):
        loc = {}
        select_query = "SELECT ID, LAT, LON, LOCATION FROM SENSOR_CONFIG WHERE ID = '" + self.client_id + "';"""
        self.cur.execute(select_query)
        records = self.cur.fetchall()

        for row in records:
            print("Id: ", row[0])
            print("latitude: ", row[1])
            print("longitude: ", row[2])
            print("place: ", row[3])
        print("hello!")

        loc['latitude'] = row[1]
        loc['longitude'] = row[2]
        loc['place'] = row[3]

        return loc

        # This method gets the weather conditions like air temperature, air moisture & rain prediction for sensor latitude & longitude

    def _getweather(self):
        weather = {}
        ll = self._getlocation()

        sensorlat = ll['latitude']
        sensorlon = ll['longitude']

        # This is final url. This is concatenation of base_url, API_key, latitude & longitude
        Final_url = BASE_URL + "appid=" + API_KEY + "&lat=" + str(sensorlat) + "&lon=" + str(
            sensorlon) + "&units=metric"
        weather_data = requests.get(Final_url).json()
        tlist = weather_data['weather'][0]
        if tlist['main'] == "Rain":
            ValueRain = "Rain"
        else:
            ValueRain = "None"
        AirTemp = weather_data['main']['temp']
        AirMoist = weather_data['main']['humidity']

        weather['ValueRain'] = ValueRain
        weather['AirTemp'] = AirTemp
        weather['AirMoist'] = AirMoist

        return weather

    # This method will publish the data on MQTT
    # Before publishing we are configuring message to be published on MQTT
    def publish(self):
        print('Begin Publish')

        self.msg_publish_loop_cntr = self.msg_publish_loop_cntr + 1
        print("Message Publish Loop Counter: ", self.msg_publish_loop_cntr)

        if self.msg_publish_loop_cntr == 1:
            sensor_anomaly_state = self._getSenorControlId()
            self._sensor_control_id = sensor_anomaly_state
        else:
            sensor_anomaly_state = self._getSenorControlId()

        sensor_grp_actuator_stat = self._getActuatorStat()

        location = self._getlocation()
        weather = self._getweather()

        sensor_grp_latitude = location['latitude']
        sensor_grp_longitude = location['longitude']
        sensor_grp_place = location['place']
        sensor_grp_weather = weather['ValueRain']
        sensor_grp_airtemp = weather['AirTemp']
        sensor_grp_airmoist = weather['AirMoist']

        if self.msg_publish_loop_cntr > 1:
           if sensor_grp_actuator_stat == 1:
              if self._sensor_control_id > 0 and self._sensor_control_id < 4:
                 self._sensor_control_id = self._sensor_control_id + 1
              else:
                 self._sensor_control_id = 0
                 
           elif sensor_grp_actuator_stat == 0:
              if self._sensor_control_id > 1 and self._sensor_control_id < 5:
                 self._sensor_control_id = self._sensor_control_id - 1
              elif self._sensor_control_id == 1:
                 self._sensor_control_id = 1
              else:
                  self._sensor_control_id = 4

           print("Sensor ControlId: ",self._sensor_control_id)

        for i in range (3):
            message = {}

            # simualte soilTemperature based on message subscription, config table
            if self._sensor_control_id == 0:
                value = float(random.randint(10, 19))
                soilTemperature = int(round(value, 1))

            elif self._sensor_control_id == 1:
                value = float(random.randint(36, 45))
                soilTemperature = int(round(value, 1))

            elif self._sensor_control_id == 2:
                value = float(random.randint(31, 35))
                soilTemperature = int(round(value, 1))

            elif self._sensor_control_id == 3:
                value = float(random.randint(26, 30))
                soilTemperature = int(round(value, 1))

            elif self._sensor_control_id == 4:
                value = float(random.randint(20, 25))
                soilTemperature = int(round(value, 1))

            # simulate soilMoisture based on simulated soilTemperature
            # severity 1
            if soilTemperature >= 35:
                value = float(random.randint(30, 44))
                soilMoisture = int(round(value, 1))

            # severity 2
            elif soilTemperature >= 30 and soilTemperature < 35:
                value = float(random.randint(45, 59))
                soilMoisture = int(round(value, 1))

            # severity 3
            elif soilTemperature >= 25 and soilTemperature < 30:
                value = float(random.randint(60, 74))
                soilMoisture = int(round(value, 1))

            # severity 4
            elif soilTemperature >= 20 and soilTemperature < 25:
                value = float(random.randint(75, 85))
                soilMoisture = int(round(value, 1))

            # severity 0
            else:
                value = float(random.randint(86, 98))
                soilMoisture = int(round(value, 1))

            timestamp = str(datetime.datetime.now())
            message['deviceid'] = self.device_id
            message['groupid'] = 4
            message['timestamp'] = timestamp
            message['soilTemperature'] = soilTemperature
            message['soilMoisture'] = soilMoisture
            message['airTemperature'] = str(sensor_grp_airtemp)
            message['airMoisture'] = str(sensor_grp_airmoist)
            message['rainForecast'] = str(sensor_grp_weather)
            message['latitude'] = str(sensor_grp_latitude)
            message['longitude'] = str(sensor_grp_longitude)
            message['place'] = str(sensor_grp_place)
            message['actuatorStat'] = sensor_grp_actuator_stat
            messageJson = json.dumps(message)
            self.myAWSIoTMQTTClient.publish(TOPIC, messageJson, 1) 
            print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
            time.sleep(15)
        print('Publish End')

    # Disconect operation for each devices
    def disconnect(self):
        self.myAWSIoTMQTTClient.disconnect()

# Main method with actual objects and method calling to publish the data in MQTT
# Again this is a minimal example that can be extended to incopporate more devices
# Also there can be different method calls as well based on the devices and their working.
if __name__ == '__main__':

    # Soil sensor device Objects
    soil_sensor_13 = AWS("SOIL_SENS_13", "SOIL_SENS_13.pem.crt", "SOIL_SENS_13.pem.key")
    soil_sensor_14 = AWS("SOIL_SENS_14", "SOIL_SENS_14.pem.crt", "SOIL_SENS_14.pem.key")
    soil_sensor_15 = AWS("SOIL_SENS_15", "SOIL_SENS_15.pem.crt", "SOIL_SENS_15.pem.key")
    soil_sensor_16 = AWS("SOIL_SENS_16", "SOIL_SENS_16.pem.crt", "SOIL_SENS_16.pem.key")

    while True:
        try:
            for sensor in (soil_sensor_13,  soil_sensor_14, soil_sensor_15, soil_sensor_16):
                sensor.publish()
        except KeyboardInterrupt:
            print("Intiate the connection closing process from AWS.")
            for sensor in (soil_sensor_13,  soil_sensor_14, soil_sensor_15, soil_sensor_16):
                sensor.disconnect()
            print("Connection closed.")
            break

