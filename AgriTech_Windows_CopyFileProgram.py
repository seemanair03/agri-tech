# !/usr/bin/env python

#Copies the root certificate, updated config.py, downloaded thing certificates and keys to respective simulator folders


import os

# choice = input("Do you want to flush certificates and keys before copying latest?")
# if choice == "Y":
#     os.system('cmd /c "del simulator\\actuator1\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\actuator2\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\actuator3\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\actuator4\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\actuator5\AmazonRootCA1.pem"')
#
#     os.system('cmd /c "del simulator\\actuator1\config.py"')
#     os.system('cmd /c "del simulator\\actuator2\config.py"')
#     os.system('cmd /c "del simulator\\actuator3\config.py"')
#     os.system('cmd /c "del simulator\\actuator4\config.py"')
#     os.system('cmd /c "del simulator\\actuator5\config.py"')
#
#     os.system('cmd /c "del simulator\\actuator1\SPRINK_ACT_1.pem.crt"')
#     os.system('cmd /c "del simulator\\actuator2\SPRINK_ACT_2.pem.crt"')
#     os.system('cmd /c "del simulator\\actuator3\SPRINK_ACT_3.pem.crt"')
#     os.system('cmd /c "del simulator\\actuator4\SPRINK_ACT_4.pem.crt"')
#     os.system('cmd /c "del simulator\\actuator5\SPRINK_ACT_5.pem.crt"')
#
#     os.system('cmd /c "del simulator\\actuator1\SPRINK_ACT_1.pem.key"')
#     os.system('cmd /c "del simulator\\actuator2\SPRINK_ACT_2.pem.key"')
#     os.system('cmd /c "del simulator\\actuator3\SPRINK_ACT_3.pem.key"')
#     os.system('cmd /c "del simulator\\actuator4\SPRINK_ACT_4.pem.key"')
#     os.system('cmd /c "del simulator\\actuator5\SPRINK_ACT_5.pem.key"')
#
#     os.system('cmd /c "del simulator\\sensorgrp1\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\sensorgrp2\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\sensorgrp3\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\sensorgrp4\AmazonRootCA1.pem"')
#     os.system('cmd /c "del simulator\\sensorgrp5\AmazonRootCA1.pem"')
#
#     os.system('cmd /c "del simulator\\sensorgrp1\config.py"')
#     os.system('cmd /c "del simulator\\sensorgrp2\config.py"')
#     os.system('cmd /c "del simulator\\sensorgrp3\config.py"')
#     os.system('cmd /c "del simulator\\sensorgrp4\config.py"')
#     os.system('cmd /c "del simulator\\sensorgrp5\config.py"')
#
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_1.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_2.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_3.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_4.pem.crt"')
#
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_5.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_6.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_7.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_8.pem.crt"')
#
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_9.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_10.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_11.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_12.pem.crt"')
#
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_13.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_14.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_15.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_16.pem.crt"')
#
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_17.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_18.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_19.pem.crt"')
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_20.pem.crt"')
#
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_1.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_2.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_3.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp1\SOIL_SENS_4.pem.key"')
#
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_5.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_6.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_7.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp2\SOIL_SENS_8.pem.key"')
#
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_9.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_10.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_11.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp3\SOIL_SENS_12.pem.key"')
#
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_13.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_14.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_15.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp4\SOIL_SENS_16.pem.key"')
#
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_17.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_18.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_19.pem.key"')
#     os.system('cmd /c "del simulator\\sensorgrp5\SOIL_SENS_20.pem.key"')
#
#     print("All certificates, keys and configs are deleted from simulator sub-folders")
#
# else:
#     print("proceeding without any deletions")



#------BEGIN COPYING------
#Copy config.py file to simulator folders
os.system('cmd /c "copy device_onboarding\config.py simulator\\actuator1"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\actuator2"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\actuator3"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\actuator4"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\actuator5"')

os.system('cmd /c "copy device_onboarding\config.py simulator\\sensorgrp1"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\sensorgrp2"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\sensorgrp3"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\sensorgrp4"')
os.system('cmd /c "copy device_onboarding\config.py simulator\\sensorgrp5"')


#Copy root certificate to simulator folders
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\actuator1"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\actuator2"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\actuator3"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\actuator4"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\actuator5"')

os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\sensorgrp1"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\sensorgrp2"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\sensorgrp3"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\sensorgrp4"')
os.system('cmd /c "copy Docs\ca\AmazonRootCA1.pem simulator\\sensorgrp5"')


#Copy downloaded thing certificates to simulator folders
os.system('cmd /c "copy Docs\certificates\SPRINK_ACT_1.pem.crt simulator\\actuator1"')
os.system('cmd /c "copy Docs\certificates\SPRINK_ACT_2.pem.crt simulator\\actuator2"')
os.system('cmd /c "copy Docs\certificates\SPRINK_ACT_3.pem.crt simulator\\actuator3"')
os.system('cmd /c "copy Docs\certificates\SPRINK_ACT_4.pem.crt simulator\\actuator4"')
os.system('cmd /c "copy Docs\certificates\SPRINK_ACT_5.pem.crt simulator\\actuator5"')

os.system('cmd /c "copy Docs\certificates\SOIL_SENS_1.pem.crt simulator\\sensorgrp1"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_2.pem.crt simulator\\sensorgrp1"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_3.pem.crt simulator\\sensorgrp1"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_4.pem.crt simulator\\sensorgrp1"')

os.system('cmd /c "copy Docs\certificates\SOIL_SENS_5.pem.crt simulator\\sensorgrp2"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_6.pem.crt simulator\\sensorgrp2"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_7.pem.crt simulator\\sensorgrp2"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_8.pem.crt simulator\\sensorgrp2"')

os.system('cmd /c "copy Docs\certificates\SOIL_SENS_9.pem.crt simulator\\sensorgrp3"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_10.pem.crt simulator\\sensorgrp3"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_11.pem.crt simulator\\sensorgrp3"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_12.pem.crt simulator\\sensorgrp3"')

os.system('cmd /c "copy Docs\certificates\SOIL_SENS_13.pem.crt simulator\\sensorgrp4"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_14.pem.crt simulator\\sensorgrp4"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_15.pem.crt simulator\\sensorgrp4"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_16.pem.crt simulator\\sensorgrp4"')

os.system('cmd /c "copy Docs\certificates\SOIL_SENS_17.pem.crt simulator\\sensorgrp5"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_18.pem.crt simulator\\sensorgrp5"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_19.pem.crt simulator\\sensorgrp5"')
os.system('cmd /c "copy Docs\certificates\SOIL_SENS_20.pem.crt simulator\\sensorgrp5"')



#Copy downloaded private keys to simulator folders
os.system('cmd /c "copy Docs\keys\private\SPRINK_ACT_1.pem.key simulator\\actuator1"')
os.system('cmd /c "copy Docs\keys\private\SPRINK_ACT_2.pem.key simulator\\actuator2"')
os.system('cmd /c "copy Docs\keys\private\SPRINK_ACT_3.pem.key simulator\\actuator3"')
os.system('cmd /c "copy Docs\keys\private\SPRINK_ACT_4.pem.key simulator\\actuator4"')
os.system('cmd /c "copy Docs\keys\private\SPRINK_ACT_5.pem.key simulator\\actuator5"')

os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_1.pem.key simulator\\sensorgrp1"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_2.pem.key simulator\\sensorgrp1"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_3.pem.key simulator\\sensorgrp1"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_4.pem.key simulator\\sensorgrp1"')

os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_5.pem.key simulator\\sensorgrp2"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_6.pem.key simulator\\sensorgrp2"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_7.pem.key simulator\\sensorgrp2"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_8.pem.key simulator\\sensorgrp2"')

os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_9.pem.key simulator\\sensorgrp3"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_10.pem.key simulator\\sensorgrp3"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_11.pem.key simulator\\sensorgrp3"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_12.pem.key simulator\\sensorgrp3"')

os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_13.pem.key simulator\\sensorgrp4"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_14.pem.key simulator\\sensorgrp4"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_15.pem.key simulator\\sensorgrp4"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_16.pem.key simulator\\sensorgrp4"')

os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_17.pem.key simulator\\sensorgrp5"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_18.pem.key simulator\\sensorgrp5"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_19.pem.key simulator\\sensorgrp5"')
os.system('cmd /c "copy Docs\keys\private\SOIL_SENS_20.pem.key simulator\\sensorgrp5"')


print("All certificates, keys and configs are copied to simulator sub-folders, now you can proceed to run the simulator")

