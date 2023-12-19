from logging import log
from pickle import NONE
import boto3
from config import *
import subprocess
import json
import glob
import time
import os

# Define max item sizes for search pages
pageSize = 2


def aws_iot_core_create_policy(detail=True):
    """"
    The purpose of this method is to create a policy to allow things to connect, publish and subcribe to AWS IoT Core.
    """

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Log Info
    logger_aws_iot_core.info("Creating a policy")

    # Step 0: Get the policies
    logger_aws_iot_core.info(f"\tStep 0: Checking policies ...")
    policies = aws_iot_core_get_all_policies()
    policies_count = len(policies["policyNames"])
    if(policies_count == 0):
        logger_aws_iot_core.info(
            f"\t\tThere are no policiy registered. Creating a new one")
        f = open(PATH_TO_POLICY, "r")
        policyDoc_str = f.read()
        policyName = "general_policy"
        # print(policyDoc_str)
        iot_client.create_policy(
            policyName='free_policy', policyDocument=policyDoc_str)
        logger_aws_iot_core.info(
            f"\t\tPolicy {policyName} is succesfully created.")

    else:
        logger_aws_iot_core.info(
            f"\t\t{policies_count} policies are found. No need to create")
        return 0

    # Create policy docuement.
    policyDoc = {}
    policyDoc["Version"] = "2012-10-17"
    policyDoc["Statement"] = {}
    policyDoc["Statement"]["Effect"] = "Allow"
    policyDoc["Statement"]["Action"] = "iot*"
    policyDoc["Statement"]["Resource"] = "*"
    policyDoc_str = json.dumps(policyDoc)


def create_provision_file():
    """
    Creates a provisioning file under /Docs/provision. This file later used to uploaded to S3 bucket
    """


    bulk_provision_file = PATH_TO_PROVISION
    f = open(bulk_provision_file, "w")
    f.close()

    # Reopen the provision data file to attend lines
    f = open(bulk_provision_file, "a")

    # Loop through things and create a provision data for each thing
    a=0
    b=0
    c=0
    d=4
    for a in range(len(THING_NAME_PREFIX)):
        for b in range(THING_COUNT[a]):
            message = {"ThingName": THING_NAME_PREFIX[a] + '_'+ str((b+1)),
                   "ThingTypeName": THING_TYPE_NAME[a], "ThingId": str((b+1)),"ThingGroups": 'Group_' + str(int((b/d)+1-c))}
            json.dump(message, f)
            f.write("\n")
        c = 1
        d = 5


    # Close the file after operation
    f.close()


def aws_list_roles():
    # Listing IAM Roles
    client = boto3.client('iam')
    response = client.list_roles()
    logger_aws_iot_core.info('Listing iam roles ...')
    for Role in response['Roles']:
        logger_aws_iot_core.info('RoleName: '+Role['RoleName'])
        logger_aws_iot_core.info('RoleArn: '+Role['Arn']+"\n")



def aws_iot_core_create_bulk_things():
    """
     Registers mupltiple things in aws iot core registery
    """
    logger_aws_iot_core.info(f"Registering bulky things ...")

    # Read provision template
    f = open(PATH_TO_PROVISIONING_TEMPLATE, "r")

    # Create Client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Step 0: Create a thing type prior to start thing registration
    logger_aws_iot_core.info(f"\tChecking thingType")
    for thingtype in THING_TYPE_NAME:
        RetreivedthingTypes = aws_iot_core_get_all_thing_types()
        if(thingtype in RetreivedthingTypes["thingTypeNames"]):
            logger_aws_iot_core.info(
                f"\t\tThing type Name {thingtype} is already present no need to crete new one.")
        else:
            iot_client.create_thing_type(thingTypeName=thingtype, thingTypeProperties={
                                        'thingTypeDescription': 'Soil' + thingtype})
    logger_aws_iot_core.info(f"\tChecking thinggroup")
    thinggroupcount = int(THING_COUNT[0]/4) + 1
    if thinggroupcount%2 == 0:
        pass
    else:
        thinggroupcount = thinggroupcount+1
    for i in range(thinggroupcount):
        thinggroups = aws_iot_core_get_all_thing_groups()
        thinggroupname = 'Group_' + str(i)
        print(thinggroups)
        if(thinggroupname in thinggroups["thinggroupName"]):
            logger_aws_iot_core.info(
            f"\t\tThing group Name {thinggroupname} is already present no need to crete new one.")
        else:
            iot_client.create_thing_group(thingGroupName=thinggroupname, thingGroupProperties={
                                     'thingGroupDescription': 'Sprinkeler group 1'})

    # Step 1: Start things registration task
    response = iot_client.start_thing_registration_task(templateBody=f.read(), inputFileBucket=BUCKET_NAME, inputFileKey=OBJ_PROVISION_FILE, roleArn=ROLE_ARN)
    taskId = response['taskId']

    # Step 2: describe_thing_registration_task
    while(1):
        response = iot_client.describe_thing_registration_task(taskId=taskId)
        response_status = response['status']
        if(response_status == "Completed"):
            logger_aws_iot_core.info(
                f"\t Status of the bulk registration task: {response['status']}")
            return True
        if(response_status == "InProgress"):
            logger_aws_iot_core.info(
                f"\t Status of the bulk registration task: {response['status']}")
        if(response_status == "Failed"):
            logger_aws_iot_core.error(
                f"\t Status of the bulk registration task: {response['status']}")
            return False
        time.sleep(1)


def aws_s3_reset():
    """"
    Resets all the buckets and contents in the specified IOT_CORE_REGION
    """

    # Create client
    s3_client = boto3.client('s3', S3_REGION)

    # Log info
    logger_aws_iot_core.info(
        f"Deleting the S3 Buckets in the IOT_CORE_REGION {S3_REGION}")

    # Step 0: List the buckets
    s3_response = s3_client.list_buckets()
    logger_aws_iot_core.info(
        f"\tListing the S3 Buckets in the IOT_CORE_REGION {S3_REGION}")
    bucket_names = []

    for bucket in s3_response['Buckets']:
        bucket_names.append(bucket['Name'])
        print(bucket_names[-1])

    # Step 1: Delete Buckets and contents
    s3 = boto3.resource('s3')
    for bucket_name in bucket_names:
        bucket = s3.Bucket(bucket_name)
        for key in bucket.objects.all():
            key.delete()
            logger_aws_iot_core.info(f"Deleting the key {key}")

        bucket.delete()
        logger_aws_iot_core.info(f"Deleting the bucket {bucket_name}")




def aws_iot_core_get_all_policies(detail=False):
    """
    returns all the policies registerd in the aws iot core
    """

    # Return parameters
    policyArns = []
    policyNames = []

    # Parameter used to count policies
    policy_count = 0

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Parameters used to count policies and search pages
    policies_count = 0
    page_count = 0

    # Log Info
    if(detail):
        logger_aws_iot_core.info("aws-iot-core: Getting policies ...")

    # Send the first request
    response = iot_client.list_policies(pageSize=pageSize)

    # Count the number of the things until no more things are present on the search pages
    while(1):
        # Increment policy count
        policies_count = policies_count + len(response['policies'])
        if(detail):
            logger_aws_iot_core.info(
                "aws-iot-core: " + f"\t\t{len(response['policies'])} policies are found on the {page_count+1}. page. Checking the next page ...")

        # Append found policies to the lists
        for policy in response['policies']:
            policyArns.append(policy['policyArn'])
            policyNames.append(policy['policyName'])

        # Increment Page number
        page_count += 1

        # Check if nextMarker is present for next search pages
        if("nextMarker" in response):
            response = iot_client.list_policies(
                pageSize=pageSize, Marker=response["nextMarker"])
        else:
            break

    if(detail):
        logger_aws_iot_core.info(
            "aws-iot-core: "+f"\t\tGetting policies is completed. In total {policy_count} policies are found.")
    return {"policyArns": policyArns, "policyNames": policyNames}


def aws_iot_core_get_all_certificates(detail=False):
    """
    returns all the certificates registered in the aws-iot-core
    """

    # Return parameters
    certificateArns = []
    certificateIds = []

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Parameter used to count certificates and search pages
    certificates_count = 0
    page_count = 0

    # Log Info
    if(detail):
        logger_aws_iot_core.info("aws-iot-core: Getting certificates ...")

    # Send the first request
    response = iot_client.list_certificates(pageSize=pageSize)

    # Count the number of the certificates until no more certificates are present on the search pages
    while(1):
        # Increment certificate count
        certificates_count = certificates_count + len(response['certificates'])

        # Append found certificates to the lists
        for certificate in response['certificates']:
            certificateArns.append(certificate['certificateArn'])
            certificateIds.append(certificate['certificateId'])

        # Print details if the 'detail'flag is set to True
        if detail:
            logger_aws_iot_core.info(json.dumps(
                response['certificates'], indent=2, default=str))

        # Increment Page number
        page_count += 1

        # Check if nextMarker is present for next search pages
        if("nextMarker" in response):
            response = iot_client.list_certificates(
                pageSize=pageSize, marker=response["nextMarker"])
        else:
            break

    if(detail):
        logger_aws_iot_core.info(
            "aws-iot-core: "+f"\t\tGetting certificates is completed. In total {certificates_count} certificates are found.")
    return {"certificateArns": certificateArns, "certificateIds": certificateIds}


def aws_iot_core_get_all_things(detail=False):
    """
    returns all the things registered in the aws-iot-core
    """

    # Return parameters
    thingNames = []
    thingArns = []

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Parameters used to count things and search pages
    things_count = 0
    page_count = 0

    # Log Info
    if(detail):
        logger_aws_iot_core.info("Getting things")

    # Send the first request
    response = iot_client.list_things(maxResults=pageSize)

    # Count the number of the things until no more things are present on the search pages
    while(1):
        # Increment thing count
        things_count = things_count + len(response['things'])
        if(detail):
            logger_aws_iot_core.info(
                f"\t{len(response['things'])} things are found on the {page_count+1}. page. Checking the next page ...")

        # Append found things to the lists
        for thing in response['things']:
            print(response)
            thingArns.append(thing['thingArn'])
            thingNames.append(thing['thingName'])

        # Increment Page number
        page_count += 1

        # Check if nextToken is present for next search pages
        if("nextToken" in response):
            response = iot_client.list_things(
                maxResults=pageSize, nextToken=response["nextToken"])
        else:
            break

    if(detail):
        logger_aws_iot_core.info(
            f"\tGetting things is completed. In total {things_count} things are found.")
    return {"thingArns": thingArns, "thingNames": thingNames}


def aws_iot_core_reset():

    # Delete all the registered things
    aws_iot_core_delete_all_things()

    # Delete all the registered certificates
    aws_iot_core_delete_all_certificates()

    # Delete all the registered policies
    aws_iot_core_delete_all_policies()


def aws_iot_core_get_all_thing_types(detail=False):
    """
    returns all the thing types registerd in the aws iot core
    """

    # Return parameters
    thingTypeNames = []
    thingTypeArns = []

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Parameter used to count thingType names
    types_count = 0
    page_count = 0

    # Log Info
    if(detail):
        logger_aws_iot_core.info("Getting thing types")

    # Send the first request
    response = iot_client.list_thing_types(maxResults=pageSize)

    # Count the number of the things until no more things are present on the search pages
    while(1):
        # Increment thing count
        types_count = types_count + len(response['thingTypes'])
        if(detail):
            logger_aws_iot_core.info(
                f"\t{types_count} thingTypes are found on the {page_count+1}. page. Checking the next page ...")

        # Append found thingTypes to the lists
        for thingType in response['thingTypes']:
            thingTypeArns.append(thingType['thingTypeArn'])
            thingTypeNames.append(thingType['thingTypeName'])

        # Increment Page number
        page_count += 1

        # Check if nextToken is present for next search pages
        if("nextToken" in response):
            response = iot_client.list_thing_types(
                maxResults=pageSize, nextToken=response["nextToken"])
        else:
            break

    if(detail):
        logger_aws_iot_core.info(
            f"\tGetting thingTypes is completed. In total {types_count} thingTypes are found.")
    return {"thingTypeArns": thingTypeArns, "thingTypeNames": thingTypeNames}




def aws_iot_core_get_all_thing_groups(detail=False):
    """
    returns all the thing groupss registerd in the aws iot core
    """

    # Return parameters
    groupName = []
    groupArn = []

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Parameter used to count thingType names
    groups_count = 0
    page_count = 0

    # Log Info
    if(detail):
        logger_aws_iot_core.info("Getting thing groups")

    # Send the first request
    response = iot_client.list_thing_groups(maxResults=pageSize)

    # Count the number of the things until no more things are present on the search pages
    while(1):
        # Increment thing count
        groups_count = groups_count + len(response['thingGroups'])
        if(detail):
            logger_aws_iot_core.info(
                f"\t{groups_count} thinggroups are found on the {page_count+1}. page. Checking the next page ...")

        # Append found thingTypes to the lists
        for thinggroups in response['thingGroups']:
            groupArn.append(thinggroups['groupArn'])
            groupName.append(thinggroups['groupName'])

        # Increment Page number
        page_count += 1

        # Check if nextToken is present for next search pages
        if("nextToken" in response):
            response = iot_client.list_thing_groups(
                maxResults=pageSize, nextToken=response["nextToken"])
        else:
            break

    if(detail):
        logger_aws_iot_core.info(
            f"\tGetting thingTypes is completed. In total {groups_count} thinggroups are found.")
    return {"thinggroupArns": groupArn, "thinggroupName": groupName}



def aws_iot_core_delete_all_policies():
    """
    Deletes all the registerd things, certificates and policies in the client IOT_CORE_REGION. 
    Doesn't delete thing types hence it takes 5 mins to delete it 

    """
    # # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Log info
    logger_aws_iot_core.info("Deleting policies ")

    # Step 0: Get the policies
    logger_aws_iot_core.info(f"\tStep 0: Checking policies ...")
    policies = aws_iot_core_get_all_policies()
    policies_count = len(policies["policyNames"])
    if(policies_count == 0):
        logger_aws_iot_core.info(
            f"\t\tThere are no policiy registered. Exiting")
        return 0
    else:
        logger_aws_iot_core.info(f"\t\t{policies_count} policies are found.")

    # Step : Deleting policies
    logger_aws_iot_core.info("\tStep 2: Deleting policies ...")
    for policyName in policies["policyNames"]:
        iot_client.delete_policy(policyName=policyName)
        logger_aws_iot_core.info(f"\t\tDeleting the policyName: {policyName}")


def aws_iot_core_create_certificates():
    """Create certificate/s for the things registered in the IoT core.

    :param set_unique: Flag to to create unique certificates for each thing or not.


    """

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Log Info
    logger_aws_iot_core.info("Creating certificates ...")

    # Step 0: Delete the existing files under Docs/keys and Docs/certificates
    logger_aws_iot_core.info(
        f"\tStep 0: Deleting existing key and certificates in the local directory")
    logger_aws_iot_core.info("\t\tDeleting private keys ...")
    for file in glob.glob("../Docs/keys/private/*"):
        logger_aws_iot_core.info("\t\tDeleting the file {file}")
        os.remove(file)

    logger_aws_iot_core.info("\t\tDeleting public keys ...")
    for file in glob.glob("../Docs/keys/public/*"):
        logger_aws_iot_core.info("\t\tDeleting the file {file}")
        os.remove(file)

    logger_aws_iot_core.info("\t\tDeleting certificates ...")
    for file in glob.glob("../Docs/certificates/*"):
        logger_aws_iot_core.info("\t\tDeleting the file {file}")
        os.remove(file)

    # Get things registered in the IoT core
    things = aws_iot_core_get_all_things(detail=False)

    # Create certificate and keys for things
    logger_aws_iot_core.info(
        f"\tStep 1: Creating the certificates for {len(things['thingNames'])} things based on configuration")
    if(SET_CERT_UNIQUE):
        for thing in things['thingNames']:
            # Create keys and certificates
            response = iot_client.create_keys_and_certificate(setAsActive=True)

            # Get the certificate and key contents
            certificateArn = response["certificateArn"]
            certificate = response["certificatePem"]
            key_public = response["keyPair"]["PublicKey"]
            key_private = response["keyPair"]["PrivateKey"]

            # log information
            logger_aws_iot_core.info(
                f"\t\tCreating the certificate {certificateArn[:50]}...")

            # Storing the private key
            f = open("../Docs/keys/private/"+thing+".pem.key", "w")
            f.write(key_private)
            f.close()

            # Storing the public key
            f = open("../Docs/keys/public/"+thing+".pem.key", "w")
            f.write(key_public)
            f.close()

            # Storing the certificate
            f = open("../Docs/certificates/"+thing+".pem.crt", "w")
            f.write(certificate)
            f.close()
    else:
        # Create keys and certificates
        response = iot_client.create_keys_and_certificate(setAsActive=True)

        # Get the certificate and key contents
        certificateArn = response["certificateArn"]
        certificate = response["certificatePem"]
        key_public = response["keyPair"]["PublicKey"]
        key_private = response["keyPair"]["PrivateKey"]

        # log information
        logger_aws_iot_core.info(
            "\t\tCreating the certificate {certificateArn[:50]}...")
        thing = "general"

        # Storing the private key
        f = open("/Docs/keys/private/"+thing+".pem.key", "w")
        f.write(key_private)
        f.close()

        # Storing the public key
        f = open("/Docs/keys/public/"+thing+".pem.key", "w")
        f.write(key_public)
        f.close()

        # Storing the certificate
        f = open("/Docs/certificates/"+thing+".pem.crt", "w")
        f.write(certificate)
        f.close()


def aws_iot_core_delete_all_certificates(detail=True):
    """
    Deletes all the registerd certificates 

    """

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Log Info
    if(detail):
        logger_aws_iot_core.info(f"Deleting certificates")

    # Step 0: Get the certificates
    logger_aws_iot_core.info(f"\tStep 0: Getting certificates ...")
    certificates = aws_iot_core_get_all_certificates(detail=False)
    certificate_count = len(certificates["certificateIds"])
    if(certificate_count == 0):
        logger_aws_iot_core.info(
            f"\t\tThere are no certificiates registered. Exiting")
        return 0
    else:
        logger_aws_iot_core.info(
            f"\t\t{certificate_count} certificates are found.")

    # Step 1: Detach things from certificates.
    logger_aws_iot_core.info(
        f"\tStep 1: Detaching associated things and certificates ...")
    for certificateArn in certificates["certificateArns"]:
        attached_things = aws_iot_core_get_all_principal_things(
            principal=certificateArn)
        for attached_thing in attached_things:
            iot_client.detach_thing_principal(
                thingName=attached_thing, principal=certificateArn)
            logger_aws_iot_core.info(
                f"\t\tDetaching thing {attached_thing} from the certificate certificate {certificateArn[:50]}...")
        if(not attached_things):
            logger_aws_iot_core.info(
                f"\t\tThere isn't any associated principal for the certificate {certificateArn[:50]}...")

    # Step 2: Delete the certificates from IoT Core registery if is there any
    logger_aws_iot_core.info(f"\tStep 2: Deleting certificates...")
    for certificateId in certificates["certificateIds"]:
        iot_client.update_certificate(
            certificateId=certificateId, newStatus='INACTIVE')
        iot_client.delete_certificate(
            certificateId=certificateId, forceDelete=True)
        logger_aws_iot_core.info(
            f"\t\tDeleting certificateId: {certificateId}")

    logger_aws_iot_core.info(f"\t\tDeleting certificates is completed.")


def aws_iot_core_get_all_principal_things(principal, detail=False):
    """
    Lists all the things associated with the specified principal.

    """

    # Return parameters
    thingNames = []

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Parameters used to count things and search pages
    things_count = 0
    page_count = 0

    # Log Info
    if(detail):
        logger_aws_iot_core.info(
            "aws-iot-core: Getting things associated with the principal ...")

    # Send the first request
    response = iot_client.list_principal_things(
        principal=principal, maxResults=pageSize)

    # Count the number of the things until no more things are present on the search pages
    while(1):
        # Increment thing count
        things_count = things_count + len(response['things'])
        if(detail):
            logger_aws_iot_core.info(
                "aws-iot-core: " + f"\t\t{len(response['things'])} things are found on the {page_count+1}. page. Checking the next page ...")

        # Append found things to the lists
        for thing in response['things']:
            thingNames.append(thing)

        # Increment Page number
        page_count += 1

        # Check if nextToken is present for next search pages
        if("nextToken" in response):
            response = iot_client.list_principal_things(
                principal=principal, maxResults=pageSize, nextToken=response["nextToken"])
        else:
            break

    if(detail):
        logger_aws_iot_core.info(
            "aws-iot-core: "+f"\t\tGetting things is completed. In total {things_count} things are found associated with the principal.")
    return thingNames


def aws_iot_core_delete_all_things(detail=True):
    """
    Deletes all the registered things from aws-iot-core registery 
    """

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Log Info
    if(detail):
        logger_aws_iot_core.info(f"Deleting things")

    # Step 0: Get the things
    logger_aws_iot_core.info(f"\tStep 0: Getting things ...")
    things = aws_iot_core_get_all_things(detail=False)
    things_count = len(things["thingNames"])
    if(things_count == 0):
        logger_aws_iot_core.info(
            f"\t\tThere are no things registered. Exiting")
        return 0
    else:
        logger_aws_iot_core.info(f"\t\t{things_count} things are found.")

    # Step 1: Detach principals associated with the things
    logger_aws_iot_core.info(
        "\tStep 1: Detaching associated things and certificates ...")
    for thingName in things["thingNames"]:
        associated_principals = iot_client.list_thing_principals(thingName=thingName)[
            "principals"]
        for associated_principal in associated_principals:
            iot_client.detach_thing_principal(
                thingName=thingName, principal=associated_principal)
            logger_aws_iot_core.info(
                f"\t\tDetaching the principal {associated_principal[:50]}... from the thingName: {thingName}")
        if(not associated_principals):
            logger_aws_iot_core.info(
                f"\t\tThere isn't any associated principal for the thing {thingName}")

    # Step 2: Deleting things from IoT Core registery
    logger_aws_iot_core.info(
        f"\tStep 2: Deleting the things from iot-core registery ...")
    for thingName in things["thingNames"]:
        iot_client.delete_thing(thingName=thingName)
        logger_aws_iot_core.info(f"\t\tDeleting thingName: {thingName}")


def aws_s3_config():
    """Upload the provision file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Create client
    s3_client = boto3.client('s3', S3_REGION)

    # Parameter used to detect if bucket is alread created
    is_bucket_exist = False

    # Log info
    logger_aws_iot_core.info("Configuring the S3 Bucket")

    # Step 0: List the buckets
    # s3_response = s3_client.list_buckets()
    # logger_aws_iot_core.info(
    #     f"\tListing the S3 Buckets in the IOT_CORE_REGION {S3_REGION}")
    #
    # for bucket in s3_response['Buckets']:
    #     if(bucket['Name'] == BUCKET_NAME):
    #         logger_aws_iot_core.info(
    #             f"\t\tFound S3 Bucket: {bucket['Name']} no need to create a new one.")
    #         is_bucket_exist = True
    #     else:
    #         logger_aws_iot_core.info(f"\t\tFound S3 Bucket: {bucket['Name']}")

    # Step 1: Create a bucket. If bucket namaspace is not unique , you need to change the name.
    if(not is_bucket_exist):
        try:
            s3_client.create_bucket(Bucket=BUCKET_NAME)
            logger_aws_iot_core.info(
                f"\tCreating a bucket {BUCKET_NAME} is created")
        except:
            logger_aws_iot_core.info(
                f"\tFailed to creating the bucket {BUCKET_NAME} since it already exist. Please change bucket name")

    # Step 2: Define an S3 object
    obj_provision_file = PROVISION_FILE_NAME

    # Step 3: Upload the provision file
    s3_client.put_object(Body=open(PATH_TO_PROVISION, 'rb'),
                         Bucket=BUCKET_NAME, Key=obj_provision_file)
    logger_aws_iot_core.info(f"\tProvision file is succesfully uploaded")

  


def aws_iot_core_attach_certificates(detail=True):
    """
    Attach certificates the things and the policy
    """

    # Create client
    iot_client = boto3.client('iot', IOT_CORE_REGION)

    # Log info
    logger_aws_iot_core.info("Attaching certificates and things ")

    thingNames = aws_iot_core_get_all_things()["thingNames"]
    certificateArns = aws_iot_core_get_all_certificates()["certificateArns"]
    policyNames = aws_iot_core_get_all_policies()["policyNames"]

    if(SET_CERT_UNIQUE):
        # Attach unique certificates to things and policy to certificates
        if(len(thingNames) == len(certificateArns)):
            for i in range(len(thingNames)):
                # Attach certificate to things
                iot_client.attach_thing_principal(
                    thingName=thingNames[i], principal=certificateArns[i])
                if(detail):
                    logger_aws_iot_core.info(
                        f"\tAttaching thing {thingNames[i]} and certificate {certificateArns[i][:50]}...")

                # Attach policy to things
                iot_client.attach_principal_policy(
                    policyName=policyNames[0], principal=certificateArns[i])
        else:
            logger_aws_iot_core.info(
                "aws-iot-core: " + "Total number of the things and certificates missmatch")

    else:
        # Attach one and only certificate to things.
        if(len(certificateArns) > 1):
            logger_aws_iot_core.error(
                "More than one certificate is registered. Can't decide which one to use.")
        else:
            for i in range(len(thingNames)):
                iot_client.attach_thing_principal(
                    thingName=thingNames[i], principal=certificateArns[0])
                iot_client.attach_principal_policy(
                    policyName=policyNames[0], principal=certificateArns[0])

