# Table of Contents
[Agri-Tech-Farm Water Management](#agri-tech-farm-water-management)
  - [Introduction](#introduction)
  - [Basic Requirements](#basic-requirements)
  - [Advanced Features](#advanced-features)
  - [Solution Design](#solution-design)
    - [AWS Identity Access Management](#aws-identity-access-management)
    - [Amazon S3 Bucket](#amazon-s3-bucket)
    - [AWS IoT Core](#aws-iot-core)
      - [Things](#things)
      - [Thing Groups](#thing-groups)
      - [Thing Types](#thing-types)
      - [Certificates](#certificates)
      - [Policies](#policies)
      - [Rules](#rules)
    - [Kinesis Data Stream](#kinesis-data-stream)
    - [AWS Lambda](#aws-lambda)
    - [DynamoDB](#dynamodb)
    - [SQLite DB](#sqlite-db)
    - [Node-Red](#node-red)
  - [Code Files](#code-files)
    - [Device Onboarding](#device-onboarding)
      - [Prerequests & Requirements](#prerequests--requirements)
      - [Execution](#execution)
      - [Steps](#steps)
        - [1) Setup working directory](#1-setup-working-directory)
        - [2) Store the AWS User creditentials](#2-store-the-aws-user-creditentials)
        - [3) Download Root Certificate](#3-download-root-certificate)
        - [4) Save the ARN of the created IAM Role `AgriTechRole` into `config.py`](#4-save-the-arn-of-the-created-iam-role-agritechrole-into-configpy)
        - [5) Update MQTT Enpoint in `config.py`](#5-update-mqtt-enpoint-in-configpy)
        - [6) Update S3 bucket name in `config.py`](#6-update-s3-bucket-name-in-configpy)
        - [7) Update Open Weather API settings in `config.py`](#7-update-open-weather-api-settings-in-configpy)
      - [Usage](#usage)
      - [How does it work ?](#how-does-it-work-)
        - [Step 0) Resetting/Deleting the AWS IoT Core(Optional)](#step-0-resettingdeleting-the-aws-iot-coreoptional)
        - [Step 1) Creating provisioning files](#step-1-creating-provisioning-files)
        - [Step 2) Configuring a S3 bucket](#step-2-configuring-a-s3-bucket)
        - [Step 3) Create things in the Iot Core registery](#step-3-create-things-in-the-iot-core-registery)
        - [Step 4) Create certificates in the Iot Core registery](#step-4-create-certificates-in-the-iot-core-registery)
        - [Step 5) Create policy](#step-5-create-policy)
        - [Step 6): Attach everything](#step-6-attach-everything)
      - [Quick Tips](#quick-tips)
    - [Database Setup](#database-setup)
    - [Lambda Code](#lambda-code)
    - [Simulator Code](#simulator-code)
    - [Simulator Utilities for Win OS](#simulator-utilitie-for-win-os)
    - [UI Code](#ui-code)
  - [End-to-End Execution](#end-to-end-execution)
    - [Step 1 - Bulk Registration](#step-1---bulk-registration)
    - [Step 2 - Generate initial Config for Sensor Groups](#step-2---generate-initial-config-for-sensor-groups)
    - [Step 3 - Copy files for Simulators](#step-3---copy-files-for-simulators)
    - [Step 4 - Create Kinesis Data Stream](#step-4---create-kinesis-data-stream)
    - [Step 5 - Create IoT Rules](#step-5---create-iot-rules)
    - [Step 6 - Add triggers to Lambda Functions](#step-6---add-triggers-to-lambda-functions)
    - [Step 7 - Subscribe to MQTT topics for testing](#step-7---subscribe-to-mqtt-topics-for-testing)
    - [Step 8 - Run Sensor Group Simulator code (1-5)](#step-8---run-sensor-group-simulator-code-1-5)
    - [Step 9 - Run Actuator Simulator code (1-5)](#step-9---run-actuator-simulator-code-1-5)
    - [Check MQTT topics and Database for Data being stored](#check-mqtt-topics-and-database-for-data-being-stored)
  - [Graphical Representation of Data - UI](#graphical-representation-of-data---ui)
- [Screenshots](#screenshots)
- [References](#references)


# Agri-Tech-Farm Water Management 
## Introduction
Help Petrichor AgriTech, to develop an innovative solution for farm water management.

Maintaining the right balance between water consumption and soil moisture management is crucial to get a good crop yield at efficient costs. We’ll develop an automatic sprinkler system based on soil and air parameters, with information coming from embedded sensors.

[< Back to table of contents](#table-of-contents)

## Basic Requirements
This is a simple system to manage and actuate sprinklers based on soil temperature and moisture in a large farm. The same setup and technology can be replicated across various farms as needed, so scale is one of the key factors. It should be deployed on AWS Cloud Computing infrastructure, for better data gathering, efficiency, and scale.

Real and simulated soil temperature & moisture sensors need to continuously feed data to the AWS Cloud, via AWS IoT Core. That data then can be streamed and acted upon accordingly. 

The system would also fetch air temperature and humidity readings of the farm location, from an open weather API.

The initial soil sensor information can be stored in a cloud database along with unique device ids and their lat/long coordinates. Similarly, information can be stored about the sprinkler locations.

The farm has a predetermined topology when it comes to sensor and sprinkler locations. Each soil sensor comes under the range of a particular sprinkler. This can be directly mapped in the system.

The system needs to continuously monitor the incoming soil and air readings. Based on a reasonable linear difference algorithm that you can define, it should decide whether a particular soil sensor location requires water. If enough soil sensors (based on a predefined percentage) mapped to a sprinkler raise an alarm, the system should send a command to the sprinkler to turn on. Similarly, it should decide when to turn them off.

The features and systems essential for the system to function are:

1. Soil sensor and sprinkler simulators
  - There should be at least 20 soil sensors and 5 sprinklers, with each sensor mapped to a particular sprinkler
  - These should be IoT Core Things publishing and receiving information.
  - You can run all of them under one process (if you prefer) on a local machine or an EC2 instance
  - (OPTIONAL) You are free to add 1, or more, real devices with temperature and moisture sensors if you have them available
2. Air temperature and humidity information of a representative lat/long based location of the farm
  - You can use https://openweathermap.org/api or any equivalent API
  - This can be directly sent to your computing solution, via an EC2 instance, local machine, or a Lambda function
3. AWS IoT Core to receive all the data, messaging back to the sprinklers, and passing the data further down to streaming and database entities
4. Database in the cloud to store raw information and decisions
  - You can use DynamoDB (preferably) or managed MongoDB/DocumentDB/MySQL/PostgreSQL (in the cloud)
5. Quick turnaround decision making (within 5 minutes)
  - You can look at a streaming and analytics solution like Kinesis along with Lambda
  - Another option can be code in Lambda or EC2 instance, periodically checking the latest readings in the database and acting accordingly
6. Ability to display (text or visual) the state of various sensor and sprinkler systems

[< Back to table of contents](#table-of-contents)
 
## Advanced Features
7. The sensors and actuators could be auto-provisioned using a program that can use AWS IoT Core APIs. You should be able to set up a soil sensor or sprinkler through the command line (or through a UI) to register a thing with a unique name, with appropriate mapping. It should deliver the necessary keys and certificates for the device to connect and transfer data.
8. Real-time visual dashboard of the activity. This can show an entity-based or a map-based view of the current sensor states and sprinkler activity
  - You can use an IoT dashboard like Node-red for a simple view.
  - You can also go for a simple but custom frontend app using Python Flask or AWS API Gateway/Lambda to serve the relevant information, in more appealing formats.
9. Long term processing to highlight data-based insights of the farm. This can include some of the following, and any other relevant analytics:
  - Areas of low and high water consumption
  - Water consumption trends based on air temperature and humidity
  - Visual representations of farm water usage patterns, with location information (pie-charts, bar-charts, bee-hives) 

[< Back to table of contents](#table-of-contents)
 
 
## Solution Design
---
### **AWS Identity Access Management**
AWS IAM has been used for all access requirements. Following two roles have been used with the mentioned policies.
```
AgriTechRole
  AWSIoTThingsRegistration
  AWSIoTLogging
  AWSIoTRuleActions
  AWSLambdaRole
  AWSLambda_FullAccess
  AmazonKinesisFullAccess
  AmazonS3FullAccess
  AmazonDynamoDBFullAccess
LambdaRole
  AdministratorAccess
```
### **Amazon S3 Bucket**
The following S3 bucket is created for loading the provisiong file
```
sniotg2
```

[< Back to table of contents](#table-of-contents)

### **AWS IoT Core**
Through bulk registration process below IoT core items are created and mapped.
#### **Things**
```
SOIL_SENS_1
SOIL_SENS_2
SOIL_SENS_3
SOIL_SENS_4
SOIL_SENS_5
SOIL_SENS_6
SOIL_SENS_7
SOIL_SENS_8
SOIL_SENS_9
SOIL_SENS_10
SOIL_SENS_11
SOIL_SENS_12
SOIL_SENS_13
SOIL_SENS_14
SOIL_SENS_15
SOIL_SENS_16
SOIL_SENS_17
SOIL_SENS_18
SOIL_SENS_19
SOIL_SENS_20

SPRINK_ACT_1
SPRINK_ACT_2
SPRINK_ACT_3
SPRINK_ACT_4
SPRINK_ACT_5

```
#### **Thing Groups**
```
Group_0
Group_1
Group_3
Group_4
Group_5
Group_6
```
#### **Thing Types**
```
ACTUATOR
SENSOR
```
#### **Certificates**
```
<List of exactly 25 Certificates>
```

#### **Policies**
```
free_policy
```
```
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "iot:*",
        "Resource": "*"
      }
    ]
  }
```

#### **Rules**
```
StoreRawData
```
[< Back to table of contents](#table-of-contents)

### **Kinesis Data Stream**
To process near realtime data Kinesis data stream is used.
```
ATDataStream
```
[< Back to table of contents](#table-of-contents)

### **AWS Lambda**
Two Lambda functions are used. One to push raw data directly to DynamoDB and another one to detect anomalies, identify severity, send sprinkler data to actuator topic. The latter also pushes data to Sprinkler Data Table for future reference and analytics. 
```
RawDataStorageFunction
AnomalyDetectionFunction
```
[< Back to table of contents](#table-of-contents)

### **DynamoDB**
Following three Tables are created
```
RawDataTable 
AnomalyTable
SprinklerDataTable
```
[< Back to table of contents](#table-of-contents)

### **SQLite DB**
This is used for storing sensor group configuration for edge computing.
```
config.db
```

[< Back to table of contents](#table-of-contents)

### **Node-Red**
Used for visual representation of the Sensor readings and Actuator Status. Local Node-Red UI running that can be accessed using below url 
```
http://127.0.0.1:1880/
```

[< Back to table of contents](#table-of-contents)

## Code Files
---
### **Device Onboarding**
Below files are used to do bulk registration
```
bulkregistration.py
config.py
main.py
general-policy.json
provisioning-data.json
provisioning-template.json
```
Here are details of how to automate registering things in bulk to AWS IoT Core.

This section provides scripts to automate **registering things in bulk** with a **fleet provisioning process** into AWS IoT Core by using the AWS SDK for Python (boto3). In addition to the tools used for the registeration process it also provides **ready to use** methods to handle things, certificates and policies in large scale numbers.

The main aim of the repository is to automate process of registering things in bulks to `AWS IoT Core` using a `fleet provisioning template` and a provision file stored in a `AWS S3 ` bucket. After succesfully deploying the example application, any number of thing(s), certificate(s), an IoT thing type and a policy will be created in the `AWS IoT Core`. Once the **Certificates, things, and policy resources** are createted, it will also attach them to each other.

[< Back to table of contents](#table-of-contents)

#### **Prerequests & Requirements**
- An AWS IAM User with  Programmatic access and following permissions policies attached.
  - `AWSS3FullAccess` ,`AWSIoTFullAccess` policies. These are the minimum permission required to run the application. 
- An IoT Service **IAM role** to allow AWS IoT Core to call other AWS services. It is necessary to use `start_thing_registration_task()` function. Created IAM role must have minimum the following permission policies attached.
  - `AWSIoTThingsRegistration (AWS managed policy)`
  - `AmazonS3ReadOnlyAccess (AWS managed policy)`

[< Back to table of contents](#table-of-contents)

#### **Execution**
For execution, simply download the repository and follow the instructions depending on your operating system.

[< Back to table of contents](#table-of-contents)

#### **Steps** 
##### 1) Setup working directory 
```
cd YOUR_WORKING_DIRECTORY

```

##### 2) Store the AWS User creditentials 
Save the AWS Access Key Id and AWS Secret Access Key into `creditentials` file under `~/.aws`

```
[default]
aws_access_key_id = REPLACE_IT_WITH_YOUR_KEY_ID
aws_secret_access_key = REPLACE_IT_WITH_YOUR_ACCESS_KEY

```

##### 3) Download Root Certificate
1. Unzip "..\AgriTech_SeemaNair_FinalSubmission.zip" 
2. Download root file

```
AmazonRootCA1.pem
```
file to 
```
"AgriTech_SeemaNair_FinalSubmission\Docs\ca" 
```
folder, using below command
```
curl -o AmazonRootCA1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem
```

##### 4) Save the ARN of the created IAM Role `AgriTechRole` into `config.py`

```
ROLE_ARN = "arn:aws:iam::xxxxx..."
```

##### 5) Update MQTT Enpoint in `config.py`

```
MQTT_ENDPOINT = REPLACE_IT_WITH_YOUR_ENDPOINT
```
##### 6) Update S3 bucket name in `config.py`

```
BUCKET_NAME = REPLACE_IT_WITH_YOUR_BUCKETNAME
```

##### 7) Update Open Weather API settings in `config.py`

```
API_KEY = REPLACE_IT_WITH_YOUR_API_KEY
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
```
You can generate the API key by registering at the website - https://openweathermap.org/api

[< Back to table of contents](#table-of-contents)

#### **Usage** 

Run the `/device_onboarding/main.py` script to register 
- Thing(s),
- Certificate(s),
- Thing Type and 
- Policy to AWS IoT Core.

After successfully execution of the `main.py` script, by default 25 Things, 25 Certificates, `Sensor` & `Actuator` named thing type and a policy named `free_policy` will be created in the AWS IoT Core. Application will also attach the created `things,certificates and policy`.

[< Back to table of contents](#table-of-contents)

#### **How does it work ?** 

The device onboarding executes as below:

##### Step 0) Resetting/Deleting the AWS IoT Core(Optional)
Although this step is marked as optional, it is a good practice use for experimenting the tools provided by this repository. Since it deletes all the registered `things,certificates and policies`, use it carefully. In order to prevent deleting important resources by accident, this feature is not implemented by default to the execution flow in the `main.py`. You can call the following method for resetting the `AWS IoT Core`.

```
aws_iot_core_reset()
```


##### Step 1) Creating provisioning files
The very first step in the execution of `main.py` is to create a `provisioning template` and a `provision file`. Provision file includes all the necessary informations for each thing. When registering the things in bulk, provisionung template and provision file are used together to register things. As an output of this method, two files are create under `secure/provision`. This operation is done by calling the method below.

```
create_provision_files()
```


##### Step 2) Configuring a S3 bucket
Once the provisioning files created locally now it is time to upload these files into `AWS S3` bucket. In order to register things in bulk, it is a **must** to upload the `provision file` to a S3 bucket.

The method below creates a bucket in your account and uploads the file into it.
```
aws_s3_config()
```


##### Step 3) Create things in the Iot Core registery

After provisioning file is created locally and provision file is uploaded into S3 bucket, things can be created in the IoT Core Registery. The  method below creates a bulk thing provisioning task.

aws_iot_core_create_bulk_things()



##### Step 4) Create certificates in the Iot Core registery
In order to connect things using the MQTT protocoll, things needed to be associated with X.509 Certificates. We can either create a different certificate for the each registered things or we can also create one certificate and share it among the things. Based on the flag `set_cert_unique`, the method below take cares to create certificates.

```
aws_iot_core_create_certificates()
```


##### Step 5) Create policy
For ensuring the connectivity features of the created things, a simple policy is also created in the IoT Core Registery called **free_policy**. This policy allows all the connection, publishing and subscribing features.

```
aws_iot_core_create_policy()
```


##### Step 6): Attach everything
Creating things, certificates and policies is not enough for connecting things to the AWS IoT Core. Final step in this application is to attach `things,certificates and the policy`. The method below handles this task.
```
aws_iot_core_attach_certificates()
```

[< Back to table of contents](#table-of-contents)

#### **Quick Tips**
- Creating large the number of objects also increases the time required to setup the resources. For experimenting the tool try to keep the number of things to be creates less than 100 to prevent excessive load on the IoT Core. Creating 1000 things takes approximetly ~20 minutes.

[< Back to table of contents](#table-of-contents)

### **Database Setup**
Setup the three tables in DynamoDB needed to execute the project. You can either use script or manually set-up the Tables (as these are just three tables). We had manually setup the three tables. 
```
RawDataTable
  Partition Key = deviceid
  Sort Key = timestamp
```

```
AnomalyTable
  Partition Key = sensorId
  Sort Key = sensortimestamp
```
```
SprinklerDataTable
  Partition Key = actuatorId
  Sort Key = ActCmdtimestamp
```

[< Back to table of contents](#table-of-contents)

### **Lambda Code**
There are two Lambda function codes and these need to be copied to AWS Lambda. Create two Lambda Functions via AWS Console UI and paste the code to these functions.
 

from 
```
\AgriTech_SeemaNair_FinalSubmission\lambda\lambda_function_AnomalyFunction.py
```
to
```
AnomalyDetectionFunction
```

And
from
```
\AgriTech_SeemaNair_FinalSubmission\lambda\lambda_function_RawDataStorageFunction.py
```
to
```
RawDataStorageFunction
```
And deploy the code in the lambda functions.

[< Back to table of contents](#table-of-contents)

### **Simulator Code**
Under the following path there are 10 sub-folders, 5 for actuators and 5 for sensor groups.
```
...\AgriTech_SeemaNair_FinalSubmission\simulator
```
Each actuator folder (1 through 5), has a python code file. Similarly each sensor group folder has a python code file.

Actuator Simulators
```
\actuator1\actuator_stat_subscribe_grp1.py
\actuator2\actuator_stat_subscribe_grp2.py
\actuator3\actuator_stat_subscribe_grp3.py
\actuator4\actuator_stat_subscribe_grp4.py
\actuator5\actuator_stat_subscribe_grp5.py
```
Sensor Group Simulators
```
\simulator1\soil_sensor_grp1_publish.py
\simulator2\soil_sensor_grp2_publish.py
\simulator3\soil_sensor_grp3_publish.py
\simulator4\soil_sensor_grp4_publish.py
\simulator5\soil_sensor_grp5_publish.py
```


*You can change sensor group Latitude and Longitude values for sensors if you want (this can be done in config.py file*

The Sensor Group Configuration is done using below python code that generates `config.db` with initial settings for severity levels (control id) and actuatuator status
```
\simulator\sensor_config_grp.py
```
This `config.db` is used by the sensor group simulators to read settings and by actuator simulators to update the settings.

[< Back to table of contents](#table-of-contents)

### **Simulator Utilitie for WIN OS**
Following additional .py files are added to help make the set-up activity faster.

If you are running simulation from a windows OS, you can run `AgriTech_Windows_CopyFileProgram.py` utility script for copying the downloaded certificates, keys and configs.

```
...\AgriTech_SeemaNair_FinalSubmission\AgriTech_Windows_CopyFileProgram.py

```
If you want to launch simulator windows you can run `AgriTech_Windows_StartSimulation.py` utility script.
*Make sure to change the mqtt endpoints in `AgriTech_Windows_StartSimulation.py` file.*
```
...\AgriTech_SeemaNair_FinalSubmission\AgriTech_Windows_StartSimulation.py

```

[< Back to table of contents](#table-of-contents)

### **UI Code**

Under the path `..\AgriTech_SeemaNair_FinalSubmission\dashboard\` you will find the JSON file for Node-Red UI.
```
node_red_dashboard_ui.json
```
update the mqtt endpoint, certificates and key in the json and then import in the Node-Red running locally.

[< Back to table of contents](#table-of-contents)

## End-to-End Execution
---

### **Step 1 - Bulk Registration**
1. Execute `..\AgriTech_SeemaNair_FinalSubmission\device_onboarding\main.py` code
2. Above execution creates things, thing groups, thing types, certificates and policy in AWS and attaches them, this also downloads the certificates and key files in below path
```
\AgriTech_SeemaNair_FinalSubmission\Docs\certificates\<list of 25 certificate files>
```
```
\AgriTech_SeemaNair_FinalSubmission\Docs\keys\private\<list of 25 private key files>
```
```
\AgriTech_SeemaNair_FinalSubmission\Docs\keys\public\<list of 25 public key files>
```

[< Back to table of contents](#table-of-contents)

### **Step 2 - Generate initial Config for Sensor Groups**
1. Execute `..\AgriTech_SeemaNair_FinalSubmission\simulator\sensor_config_grp.py` code
2. Above execution generates `..\AgriTech_SeemaNair_FinalSubmission\simulator\config.db`

[< Back to table of contents](#table-of-contents)

### **Step 3 - Copy files for Simulators**
1. Copy the root file `AmazonRootCA1.pem` from `\AgriTech_SeemaNair_FinalSubmission\Docs\ca\` to all the simulator sub-folders
2. Copy the `config.py` file from `\AgriTech_SeemaNair_FinalSubmission\device_onboarding\` to all the simulator sub-folders
3. Copy the certificates from `\AgriTech_SeemaNair_FinalSubmission\Docs\certificates\` to the respective simulator sub-folders
4. Copy the private keys from `\AgriTech_SeemaNair_FinalSubmission\Docs\keys\private\` to the respective simulator sub-folders.

Now each of the actuator sub-folders (1 through 5) must have below files (showing actuator1 sub-folder contents below):-
```
actuator_stat_subscribe_grp1.py
AmazonRootCA1.pem
config.py
SPRINK_ACT_1.pem
SPRINK_ACT_1.pem.key
```

and each of the sensor group sub-folders (1 through 5) must have below files (showing sensorgrp1 sub-folder contents below):-
```
soil_sensor_grp1_publish.py
AmazonRootCA1.pem
config.py
SOIL_SENS_1.pem
SOIL_SENS_2.pem
SOIL_SENS_3.pem
SOIL_SENS_4.pem
SOIL_SENS_1.pem.key
SOIL_SENS_2.pem.key
SOIL_SENS_3.pem.key
SOIL_SENS_4.pem.key
```
Copying can be done programatically or manually based on the count of sensors and actuators.

*Check section [Simulator Help Files](#simulator-help-files) for prgramatically copying files on windows OS*

[< Back to table of contents](#table-of-contents)

### **Step 4 - Create Kinesis Data Stream**
`ATDataStream`


### **Step 5 - Create IoT Rules**
IoT Rule has to be set so that raw data from iot/agritech topic can be posted to Kinesis Data Stream and to Lambda function.
  1. Create IoT Rule `StoreRawData` to post data from topic  `iot/agritech` to `ATDataStream` Kinesis Data Stream (set partition key as deviceid), and also to post same incoming data to `RawDataStorageFunction` Lambda function.
  
  SQL Statement
  ```
  SELECT * FROM 'iot/agritech'
  ```
  Rule actions
  

  
  Action 1
  ```
  Kinesis Stream
  ```
  Stream name
  ```
  ATDataStream
  ```
  Partition key
  ```
  deviceid
  ```
  IAM Role
  ```
  AgriTechRole
  ```

  Action 2
  ```
  Lambda
  ```
  Lambda Function
  ```
  RawDataStorageFunction
  ```


[< Back to table of contents](#table-of-contents)


### **Step 6 - Add triggers to Lambda Functions**
- Add Kinesis Data Stream `ATDataStream` as trigger to `AnomalyDetectionFunction`.

- Add `AWS IoT` trigger to `RawDataStorageFunction`
  Select Rule `StoreRawData`

[< Back to table of contents](#table-of-contents)

### **Step 7 - Subscribe to MQTT topics for testing**
Subscribe to below MQTT topics
```
iot/agritech
iot/actuatorstat
```

[< Back to table of contents](#table-of-contents)

### **Step 8 - Run Sensor Group Simulator code (1-5)**

*If you are using windows you can refer [Simulator Help Files](#simulator-help-files) for one click run*

Execute below code files simultaneously in separate terminals:-

Terminal 1
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\simulator1\

python soil_sensor_grp1_publish.py
```
Terminal 2
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\simulator2\

python soil_sensor_grp2_publish.py
```
Terminal 3
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\simulator3\

python soil_sensor_grp3_publish.py
```
Terminal 4
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\simulator4\

python soil_sensor_grp4_publish.py
```
Terminal 5
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\simulator5\

python soil_sensor_grp5_publish.py
```

[< Back to table of contents](#table-of-contents)

### **Step 9 - Run Actuator Simulator code (1-5)**
*If you are using windows you can refer [Simulator Help Files](#simulator-help-files) for one click run*

Execute bwlow commands simultaneously in separate command windows:-


Command Window1
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\actuator1\

python actuator_stat_subscribe_grp1.py -e ajta2yw0ktjf6-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_1.pem.crt -k SPRINK_ACT_1.pem.key -id SPRINK_ACT_1 -t iot/actuatorstat
```
Command Window2
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\actuator2\

python actuator_stat_subscribe_grp2.py -e ajta2yw0ktjf6-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_2.pem.crt -k SPRINK_ACT_2.pem.key -id SPRINK_ACT_2 -t iot/actuatorstat
```
Command Window 3
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\actuator3\

python actuator_stat_subscribe_grp3.py -e ajta2yw0ktjf6-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_3.pem.crt -k SPRINK_ACT_3.pem.key -id SPRINK_ACT_3 -t iot/actuatorstat
```
Command Window 4
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\actuator4\

python actuator_stat_subscribe_grp4.py -e ajta2yw0ktjf6-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_4.pem.crt -k SPRINK_ACT_4.pem.key -id SPRINK_ACT_4 -t iot/actuatorstat
```
Command Window 5
```
cd \AgriTech_SeemaNair_FinalSubmission\simulator\actuator5\

python actuator_stat_subscribe_grp5.py -e ajta2yw0ktjf6-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_5.pem.crt -k SPRINK_ACT_5.pem.key -id SPRINK_ACT_5 -t iot/actuatorstat
```


[< Back to table of contents](#table-of-contents)

### **Check MQTT topics and Database for Data being stored**

1. Go to IoT Core and check both the topics:-
  - `iot/agritech` for data posted by sensor simulators and
  - `iot/actuatorstat` for data posted by lambda function that has sprinkler status.

2. Go to `RawDataTable`, `AnomalyTable` & `SprinklerDataTable` for data being stored.

3. You can also review the Monitor tab of both Lambda functions for data being fetched and put.

4. Sensor Simulator command windows show the sensor data flowing from sensor simulators to the `iot/agritech` topic.

5. Actuator Simulator command windows (aka Listener/Subscriber) show the command data flowing from server to the actuators (via `iot/actuatorstat` topic).

[< Back to table of contents](#table-of-contents)

## Graphical Representation of Data - UI
1. Start Node-Red locally using below command
```
node-red
```
2. Launch Node-Red UI using below link (or similar link provided on cmd prompt after node-red server launches locally).
```
http://127.0.0.1:1880/
``` 
3. Navigate to Dashboard to view tab `Agritech Dashboard`.


[< Back to table of contents](#table-of-contents)

# Screenshots
Refer below location for screenshots captured during the entire project setup & execution.
```
\AgriTech_SeemaNair_FinalSubmission\Screenshots
```

# References
1. Bulk Registration Process sample code - https://www.youtube.com/watch?v=F2GZ7tHtGAI
2. Node-Red - https://nodered.org/
3. AWS Architecture Diagrams - https://aws.amazon.com/architecture/icons/  
4. SQLite - https://www.sqlite.org/index.html 


[< Back to table of contents](#table-of-contents)

