import sys
import logging

# Local directory paths and file names
PROVISION_FILE_NAME = "provisioning-data.json"
POLICY_FILE_NAME = "general-policy.json"
PROVISIONING_TEMPLATE = "provisioning-template.json"

PATH_TO_PROVISION = '../Docs/provision/' + PROVISION_FILE_NAME
PATH_TO_POLICY = '../Docs/policy/' + POLICY_FILE_NAME
PATH_TO_PROVISIONING_TEMPLATE = '../Docs/provision/' + PROVISIONING_TEMPLATE

# AWS IoT Core Region
IOT_CORE_REGION = "us-east-1"

# AWS IoT Core - Parameters used for creating thing(s) and thing type
THING_TYPE_NAME = ["SENSOR", "ACTUATOR"]
THING_NAME_PREFIX = ['SOIL_SENS', 'SPRINK_ACT']
THING_COUNT = [20, 5]

# AWS IoT Core - Parameters used for the MQTT Connection
MQTT_ENDPOINT = "ajta2yw0ktjf6-ats.iot.us-east-1.amazonaws.com"
#MQTT_ENDPOINT = "a3fhbju8xoji12-ats.iot.us-east-1.amazonaws.com"
PATH_TO_ROOT_CA = "AmazonRootCA1.pem"
MQTT_PORT = 8883
MQTT_TOPIC = "iot/agritech"

# AWS IoT Core - Parameter used for creating certificates(s)
SET_CERT_UNIQUE = True

# AWS S3 - Paremeters used to set up a  S3 bucket
S3_REGION = "us-east-1"
ROLE_ARN = "arn:aws:iam::337953792932:role/AgriTechRole"
#ROLE_ARN = "arn:aws:iam::862085834875:role/AgriTechRole"
BUCKET_NAME = "sniot"

OBJ_PROVISION_FILE = PROVISION_FILE_NAME

# Open Weather API Connection configs.
API_KEY = "d8d61866df37c68cbc84558495e5b5d1"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Logger Settings
logger_aws_iot_core = logging.getLogger('example_logger')
logger_aws_iot_core.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler_aws_iot_core = logging.StreamHandler(sys.stdout)
log_format_aws_iot_core = logging.Formatter('%(asctime)s - %(levelname)s - AWS-IOT-CORE - %(message)s',
                                            datefmt='%H:%M:%S')
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
handler_aws_iot_core.setFormatter(log_format_aws_iot_core)
handler.setFormatter(log_format)
logger_aws_iot_core.addHandler(handler_aws_iot_core)
