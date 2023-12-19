from decimal import Decimal
from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random
import base64
import os
import sys


def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    # Anomaly Data logging function

    def Anomalylogger(sensid, soiltemp, soilmoist, grpid, actstat, grpanostat, sensTimestamp, sensLat, sensLon, sensplace):
        message = {}
        actuatortimestamp = str(datetime.datetime.now())
        if grpid == 1:
            message['actuatorId'] = "SPRINK_ACT_1"
            message['sensorId'] = sensid
            message['soilTemperature'] = soiltemp
            message['soilMoisture'] = soilmoist
            message['grouprId'] = grpid
            message['actuatorStat'] = actstat
            message['grpAnomalyState'] = grpanostat
            message['actReqtimestamp'] = actuatortimestamp
            message['sensortimestamp'] = sensTimestamp
            message['sensorlatitude'] = sensLat
            message['sensorlongitude'] = sensLon
            message['sensorplace'] = sensplace
            payloadmessage = json.dumps(message)
            table = dynamodb_res.Table('AnomalyTable')
            responseAnomaly = table.put_item(Item=message)
        elif grpid == 2:
            message['actuatorId'] = "SPRINK_ACT_2"
            message['sensorId'] = sensid
            message['soilTemperature'] = soiltemp
            message['soilMoisture'] = soilmoist
            message['grouprId'] = grpid
            message['actuatorStat'] = actstat
            message['grpAnomalyState'] = grpanostat
            message['actReqtimestamp'] = actuatortimestamp
            message['sensortimestamp'] = sensTimestamp
            message['sensorlatitude'] = sensLat
            message['sensorlongitude'] = sensLon
            message['sensorplace'] = sensplace
            payloadmessage = json.dumps(message)
            table = dynamodb_res.Table('AnomalyTable')
            responseAnomaly = table.put_item(Item=message)
        elif grpid == 3:
            message['actuatorId'] = "SPRINK_ACT_3"
            message['sensorId'] = sensid
            message['soilTemperature'] = soiltemp
            message['soilMoisture'] = soilmoist
            message['grouprId'] = grpid
            message['actuatorStat'] = actstat
            message['grpAnomalyState'] = grpanostat
            message['actReqtimestamp'] = actuatortimestamp
            message['sensortimestamp'] = sensTimestamp
            message['sensorlatitude'] = sensLat
            message['sensorlongitude'] = sensLon
            message['sensorplace'] = sensplace
            payloadmessage = json.dumps(message)
            table = dynamodb_res.Table('AnomalyTable')
            responseAnomaly = table.put_item(Item=message)
        elif grpid == 4:
            message['actuatorId'] = "SPRINK_ACT_4"
            message['sensorId'] = sensid
            message['soilTemperature'] = soiltemp
            message['soilMoisture'] = soilmoist
            message['grouprId'] = grpid
            message['actuatorStat'] = actstat
            message['grpAnomalyState'] = grpanostat
            message['actReqtimestamp'] = actuatortimestamp
            message['sensortimestamp'] = sensTimestamp
            message['sensorlatitude'] = sensLat
            message['sensorlongitude'] = sensLon
            message['sensorplace'] = sensplace
            payloadmessage = json.dumps(message)
            table = dynamodb_res.Table('AnomalyTable')
            responseAnomaly = table.put_item(Item=message)
        elif grpid == 5:
            message['actuatorId'] = "SPRINK_ACT_5"
            message['sensorId'] = sensid
            message['soilTemperature'] = soiltemp
            message['soilMoisture'] = soilmoist
            message['grouprId'] = grpid
            message['actuatorStat'] = actstat
            message['grpAnomalyState'] = grpanostat
            message['actReqtimestamp'] = actuatortimestamp
            message['sensortimestamp'] = sensTimestamp
            message['sensorlatitude'] = sensLat
            message['sensorlongitude'] = sensLon
            message['sensorplace'] = sensplace
            payloadmessage = json.dumps(message)
            table = dynamodb_res.Table('AnomalyTable')
            responseAnomaly = table.put_item(Item=message)

    # Actuator Command Generator function

    def ActuatorCommandLogger(votingactreq, grpid, rainForecast, anomalystate, sensLat, sensLon, sensplace):
        ActCmdMsg = {}
        ActCmdTimestamp = str(datetime.datetime.now())
        if (votingactreq >= 3) and (rainForecast == "None"):
            print(rainForecast)
            if grpid == 1:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_1"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 1
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)

            elif grpid == 2:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_2"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 1
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)

            elif grpid == 3:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_3"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 1
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)

            elif grpid == 4:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_4"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 1
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)
            elif grpid == 5:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_5"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 1
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)
            else:
                pass

        elif votingactreq <= 1:

            if grpid == 1:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_1"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 0
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)
                data = tableSprinkler.scan()
            elif grpid == 2:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_2"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 0
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)
                data = tableSprinkler.scan()
            elif grpid == 3:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_3"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 0
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)
                data = tableSprinkler.scan()
            elif grpid == 4:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_4"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 0
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)
                data = tableSprinkler.scan()
            elif grpid == 5:
                ActCmdMsg['actuatorId'] = "SPRINK_ACT_5"
                ActCmdMsg['groupId'] = int(grpid)
                ActCmdMsg['actuatorCmd'] = 0
                ActCmdMsg['grpAnomalyState'] = int(anomalystate)
                ActCmdMsg['ActCmdtimestamp'] = ActCmdTimestamp
                ActCmdMsg['rainForecast'] = rainForecast
                ActCmdMsg['sensorLatitude'] = sensLat
                ActCmdMsg['sensorLongitude'] = sensLon
                ActCmdMsg['sensorplace'] = sensplace
                payloadmessage = json.dumps(ActCmdMsg)
                client = boto3.client('iot-data', region_name='us-east-1')
                tableSprinkler = dynamodb_res.Table('SprinklerDataTable')
                UpdateSprinkTabOFF = tableSprinkler.put_item(Item=ActCmdMsg)
                responsemessage = client.publish(topic='iot/actuatorstat', qos=0, payload=payloadmessage)
                data = tableSprinkler.scan()
            else:
                pass
        else:
            pass

    for record in event['Records']:
        print("verify timestamp")
        payload = base64.b64decode(record["kinesis"]["data"])
        payload = str(payload, 'utf-8')
        pprint(payload, sort_dicts=False)
        eventtxt = json.loads(payload)
        table = dynamodb_res.Table('AnomalyTable')

        # Voting Logic & Anomaly Detection for Group 1 set of Devices

        data = table.scan()
        responsequery11 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_1", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery12 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_2", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery13 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_3", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery14 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_4", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        recordcount1 = responsequery11['Count'] + responsequery12['Count'] + responsequery13['Count'] + responsequery14[
            'Count']
        if recordcount1 == 4:
            VotinggrpAnomalyStateList1 = [0, 0, 0, 0]
            VotinggrpAnomalyStateList1[0] = responsequery11['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList1[1] = responsequery12['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList1[2] = responsequery13['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList1[3] = responsequery14['Items'][0].get('grpAnomalyState')
            grp1AnomalyStateMax = max(VotinggrpAnomalyStateList1)
            VotingActReq1 = responsequery11['Items'][0].get('actuatorStat') + responsequery12['Items'][0].get(
                'actuatorStat') + responsequery13['Items'][0].get('actuatorStat') + responsequery14['Items'][0].get(
                'actuatorStat')

            ActuatorCommandLogger(VotingActReq1, 1, eventtxt['rainForecast'], grp1AnomalyStateMax, eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass

        if ((eventtxt['soilTemperature'] in range(20, 25)) or (eventtxt['soilMoisture'] in range(75, 86))) and (
                eventtxt['groupid'] == 1):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 4, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'] )

        elif ((eventtxt['soilTemperature'] in range(0, 20)) or (eventtxt['soilMoisture'] in range(86, 101))) and (
                eventtxt['groupid'] == 1):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 0, 0, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(25, 30)) or (eventtxt['soilMoisture'] in range(60, 75))) and (
                eventtxt['groupid'] == 1):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 3, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(30, 35)) or (eventtxt['soilMoisture'] in range(45, 60))) and (
                eventtxt['groupid'] == 1):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 2, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] >= 35) or (eventtxt['soilMoisture'] < 30)) and (eventtxt['groupid'] == 1):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 1, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass

        # Voting Logic & Anomaly Detection for Group 2 set of Devices

        data = table.scan()
        responsequery21 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_5", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery22 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_6", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery23 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_7", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery24 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_8", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        recordcount2 = responsequery21['Count'] + responsequery22['Count'] + responsequery23['Count'] + responsequery24[
            'Count']
        print(recordcount2)
        if recordcount2 == 4:
            VotinggrpAnomalyStateList2 = [0, 0, 0, 0]
            VotinggrpAnomalyStateList2[0] = responsequery21['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList2[1] = responsequery22['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList2[2] = responsequery23['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList2[3] = responsequery24['Items'][0].get('grpAnomalyState')
            grp2AnomalyStateMax = max(VotinggrpAnomalyStateList2)
            VotingActReq2 = responsequery21['Items'][0].get('actuatorStat') + responsequery22['Items'][0].get(
                'actuatorStat') + responsequery23['Items'][0].get('actuatorStat') + responsequery24['Items'][0].get(
                'actuatorStat')
            ActuatorCommandLogger(VotingActReq2, 2, eventtxt['rainForecast'], grp2AnomalyStateMax, eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass

        if ((eventtxt['soilTemperature'] in range(20, 25)) or (eventtxt['soilMoisture'] in range(75, 86))) and (
                eventtxt['groupid'] == 2):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 4, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(0, 20)) or (eventtxt['soilMoisture'] in range(86, 101))) and (
                eventtxt['groupid'] == 2):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 0, 0, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(25, 30)) or (eventtxt['soilMoisture'] in range(60, 75))) and (
                eventtxt['groupid'] == 2):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 3, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(30, 35)) or (eventtxt['soilMoisture'] in range(45, 60))) and (
                eventtxt['groupid'] == 2):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 2, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] >= 35) or (eventtxt['soilMoisture'] < 30)) and (eventtxt['groupid'] == 2):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 1, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass

        # Voting Logic & Anomaly Detection for Group 3 set of Devices

        data = table.scan()
        responsequery31 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_9", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery32 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_10", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery33 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_11", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery34 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_12", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        recordcount3 = responsequery31['Count'] + responsequery32['Count'] + responsequery33['Count'] + responsequery34[
            'Count']
        if recordcount3 == 4:
            VotinggrpAnomalyStateList3 = [0, 0, 0, 0]
            VotinggrpAnomalyStateList3[0] = responsequery31['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList3[1] = responsequery32['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList3[2] = responsequery33['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList3[3] = responsequery34['Items'][0].get('grpAnomalyState')
            grp3AnomalyStateMax = max(VotinggrpAnomalyStateList3)
            VotingActReq3 = responsequery31['Items'][0].get('actuatorStat') + responsequery32['Items'][0].get(
                'actuatorStat') + responsequery33['Items'][0].get('actuatorStat') + responsequery34['Items'][0].get(
                'actuatorStat')
            ActuatorCommandLogger(VotingActReq3, 3, eventtxt['rainForecast'], grp3AnomalyStateMax, eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass
        if ((eventtxt['soilTemperature'] in range(20, 25)) or (eventtxt['soilMoisture'] in range(75, 86))) and (
                eventtxt['groupid'] == 3):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 4, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(0, 20)) or (eventtxt['soilMoisture'] in range(86, 101))) and (
                eventtxt['groupid'] == 3):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 0, 0, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(25, 30)) or (eventtxt['soilMoisture'] in range(60, 75))) and (
                eventtxt['groupid'] == 3):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 3, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(30, 35)) or (eventtxt['soilMoisture'] in range(45, 60))) and (
                eventtxt['groupid'] == 3):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 2, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] >= 35) or (eventtxt['soilMoisture'] < 30)) and (eventtxt['groupid'] == 3):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 1, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass

        # Voting Logic & Anomaly Detection for Group 4 set of Devices

        data = table.scan()
        responsequery41 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_13", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery42 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_14", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery43 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_15", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery44 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_16", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        recordcount4 = responsequery41['Count'] + responsequery42['Count'] + responsequery43['Count'] + responsequery44[
            'Count']
        if recordcount4 == 4:
            VotinggrpAnomalyStateList4 = [0, 0, 0, 0]
            VotinggrpAnomalyStateList4[0] = responsequery41['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList4[1] = responsequery42['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList4[2] = responsequery43['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList4[3] = responsequery44['Items'][0].get('grpAnomalyState')
            grp4AnomalyStateMax = max(VotinggrpAnomalyStateList4)
            VotingActReq4 = responsequery41['Items'][0].get('actuatorStat') + responsequery42['Items'][0].get(
                'actuatorStat') + responsequery43['Items'][0].get('actuatorStat') + responsequery44['Items'][0].get(
                'actuatorStat')
            ActuatorCommandLogger(VotingActReq4, 4, eventtxt['rainForecast'], grp4AnomalyStateMax, eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass
        if ((eventtxt['soilTemperature'] in range(20, 25)) or (eventtxt['soilMoisture'] in range(75, 86))) and (
                eventtxt['groupid'] == 4):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 4, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(0, 20)) or (eventtxt['soilMoisture'] in range(86, 101))) and (
                eventtxt['groupid'] == 4):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 0, 0, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(25, 30)) or (eventtxt['soilMoisture'] in range(60, 75))) and (
                eventtxt['groupid'] == 4):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 3, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(30, 35)) or (eventtxt['soilMoisture'] in range(45, 60))) and (
                eventtxt['groupid'] == 4):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 2, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] >= 35) or (eventtxt['soilMoisture'] < 30)) and (eventtxt['groupid'] == 4):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 1, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass

        # Voting Logic & Anomaly Detection for Group 5 set of Devices

        data = table.scan()
        responsequery51 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_17", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery52 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_18", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery53 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_19", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        responsequery54 = table.query(KeyConditionExpression='sensorId = :hkey',
                                      ExpressionAttributeValues={':hkey': "SOIL_SENS_20", }, Limit=1,
                                      ProjectionExpression='grpAnomalyState,grouprId,actuatorStat,sensortimestamp',
                                      ScanIndexForward=False)
        recordcount5 = responsequery51['Count'] + responsequery52['Count'] + responsequery53['Count'] + responsequery54[
            'Count']
        if recordcount5 == 4:
            VotinggrpAnomalyStateList5 = [0, 0, 0, 0]
            VotinggrpAnomalyStateList5[0] = responsequery51['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList5[1] = responsequery52['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList5[2] = responsequery53['Items'][0].get('grpAnomalyState')
            VotinggrpAnomalyStateList5[3] = responsequery54['Items'][0].get('grpAnomalyState')
            grp5AnomalyStateMax = max(VotinggrpAnomalyStateList5)
            VotingActReq5 = responsequery51['Items'][0].get('actuatorStat') + responsequery52['Items'][0].get(
                'actuatorStat') + responsequery53['Items'][0].get('actuatorStat') + responsequery54['Items'][0].get(
                'actuatorStat')
            ActuatorCommandLogger(VotingActReq5, 5, eventtxt['rainForecast'], grp5AnomalyStateMax, eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass
        if ((eventtxt['soilTemperature'] in range(20, 25)) or (eventtxt['soilMoisture'] in range(75, 86))) and (
                eventtxt['groupid'] == 5):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 4, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(0, 20)) or (eventtxt['soilMoisture'] in range(86, 101))) and (
                eventtxt['groupid'] == 5):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 0, 0, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(25, 30)) or (eventtxt['soilMoisture'] in range(60, 75))) and (
                eventtxt['groupid'] == 5):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 3, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] in range(30, 35)) or (eventtxt['soilMoisture'] in range(45, 60))) and (
                eventtxt['groupid'] == 5):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 2, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])

        elif ((eventtxt['soilTemperature'] >= 35) or (eventtxt['soilMoisture'] < 30)) and (eventtxt['groupid'] == 5):
            Anomalylogger(eventtxt['deviceid'], eventtxt['soilTemperature'], eventtxt['soilMoisture'],
                          eventtxt['groupid'], 1, 1, eventtxt['timestamp'], eventtxt['latitude'], eventtxt['longitude'], eventtxt['place'])
        else:
            pass

