# !/usr/bin/env python
#Starts all 5 Sensor Groups and all 5 Actuator simulators.
import os

# #Start Simulator 1
# os.system('cmd /c "cd simulator/sensorgrp1 & start "Sensor Group 1" python soil_sensor_grp1_publish.py"')
# os.system('cmd /c "cd simulator/actuator1 & start "Actuator 1" python actuator_stat_subscribe_grp1.py -e a3fhbju8xoji12-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_1.pem.crt -k SPRINK_ACT_1.pem.key -id SPRINK_ACT_1 -t iot/actuatorstat"')
# print("Simulator 1 Started!")


#
# #Start Simulator 2
# os.system('cmd /c "cd simulator/sensorgrp2 & start "Sensor Group 2" python soil_sensor_grp2_publish.py"')
# os.system('cmd /c "cd simulator/actuator2 & start "Actuator 2" python actuator_stat_subscribe_grp2.py -e a3fhbju8xoji12-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_2.pem.crt -k SPRINK_ACT_2.pem.key -id SPRINK_ACT_2 -t iot/actuatorstat"')
# print("Simulator 2 Started!")


# #Start Simulator 3
# os.system('cmd /c "cd simulator/sensorgrp3 & start "Sensor Group 3" python soil_sensor_grp3_publish.py"')
# os.system('cmd /c "cd simulator/actuator3 & start "Actuator 3" python actuator_stat_subscribe_grp3.py -e a3fhbju8xoji12-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_3.pem.crt -k SPRINK_ACT_3.pem.key -id SPRINK_ACT_3 -t iot/actuatorstat"')
# print("Simulator 3 Started!")



#Start Simulator 4
os.system('cmd /c "cd simulator/sensorgrp4 & start "Sensor Group 4" python soil_sensor_grp4_publish.py"')
os.system('cmd /c "cd simulator/actuator4 & start "Actuator 4" python actuator_stat_subscribe_grp4.py -e a3fhbju8xoji12-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_4.pem.crt -k SPRINK_ACT_4.pem.key -id SPRINK_ACT_4 -t iot/actuatorstat"')
print("Simulator 4 Started!")


# #Start Simulator 5
# os.system('cmd /c "cd simulator/sensorgrp5 & start "Sensor Group 5" python soil_sensor_grp5_publish.py"')
# os.system('cmd /c "cd simulator/actuator5 & start "Actuator 5" python actuator_stat_subscribe_grp5.py -e a3fhbju8xoji12-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c SPRINK_ACT_5.pem.crt -k SPRINK_ACT_5.pem.key -id SPRINK_ACT_5 -t iot/actuatorstat"')
# print("Simulator 5 Started!")





