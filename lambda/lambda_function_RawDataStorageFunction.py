import json
from pprint import pprint
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
import subprocess


def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')
    print(event)
    eventtxt = json.dumps(event)
        
    table = dynamodb_res.Table('RawDataTable')
    response = table.put_item(Item=event)