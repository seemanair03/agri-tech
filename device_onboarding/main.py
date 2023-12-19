from config import *
from bulkregistration import *
from sys import exit

if __name__ == "__main__":

    # Step 1: Create a provision file
    create_provision_file()

    # Step 2: Configure the s3 bucket
    aws_s3_config()

    # Step 3: Create things in the Iot Core registry
    status = aws_iot_core_create_bulk_things()
    if not status: exit

    # Step 4: Create certificates in the Iot Core registry
    aws_iot_core_create_certificates()

    # Step 6: Create policy
    aws_iot_core_create_policy()

    # Step 7: Attach everything
    aws_iot_core_attach_certificates()
    Data = open(PATH_TO_PROVISION, "r")
    print(Data)
