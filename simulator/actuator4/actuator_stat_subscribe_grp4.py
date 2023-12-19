'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

 * This  File is modified by GreatLearning.in for the educational purposes.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_OPERATION_TIMEOUT_SEC
import logging
import datetime
import argparse
import json
import random
import csv
import time
import sched
import sqlite3

AllowedActions = ['subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    messageJson ={}
    print("Received a new message: ")
    messageJson = json.loads(message.payload)
    conn = sqlite3.connect('..//config.db')
    print("Opened database successfully");

    # create cursor object
    cur = conn.cursor()
    
    grpAnomalyState = str(messageJson['grpAnomalyState'])
    actuatorStat = str(messageJson['actuatorCmd'])
    grpId_ref = messageJson['groupId']

    if grpId_ref == 1:    
      update_query1 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_1';"
      update_query2 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_2';"
      update_query3 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_3';"
      update_query4 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_4';"
    elif grpId_ref == 2:    
      update_query1 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_5';"
      update_query2 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_6';"
      update_query3 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_7';"
      update_query4 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_8';"
    elif grpId_ref == 3:    
      update_query1 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_9';"
      update_query2 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_10';"
      update_query3 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_11';"
      update_query4 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_12';"
    elif grpId_ref == 4:    
      update_query1 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_13';"
      update_query2 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_14';"
      update_query3 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_15';"
      update_query4 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_16';"
    elif grpId_ref ==5:
      update_query1 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_17';"
      update_query2 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_18';"
      update_query3 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_19';"
      update_query4 = "UPDATE SENSOR_CONFIG SET CONTROLID=" + grpAnomalyState + ", ACTUATORSTAT=" + actuatorStat + " WHERE ID='SOIL_SENS_20';"
   

    cur.execute(update_query1)
    cur.execute(update_query2)
    cur.execute(update_query3)
    cur.execute(update_query4)
    
    conn.commit()
    conn.close()
        
    print(messageJson)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="subscribe",
                    help="Operation modes: %s" % str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

while True:
    try:
        time.sleep(2)

    except KeyboardInterrupt:
        print("Intiate the connection closing process from AWS.")
        myAWSIoTMQTTClient.disconnect()
