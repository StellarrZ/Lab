import boto3
import time
from botocore.exceptions import ClientError
# import sagemaker
# print(sagemaker.get_execution_role())
 
client = boto3.client("sts")
account = client.get_caller_identity()["Account"]
print("AWS account: %s" % account)
 
session = boto3.session.Session()
region = session.region_name
print("AWS region: %s" % region)
 
# credentials = client.assume_role(
#   RoleArn="arn:aws:iam::***",
#   RoleSessionName="AssumedSession"
# )["Credentials"]

# client = boto3.client(
#   "ec2",
#   aws_access_key_id=credentials['AccessKeyId'],
#   aws_secret_access_key=credentials['SecretAccessKey'],
#   aws_session_token=credentials['SessionToken']
# )

client = boto3.client("ec2")
# zones = ['us-east-1a', 'us-east-1b']
# zones = ['us-west-2a', 'us-west-2b', 'us-west-2c', 'us-west-2d']
zones = ['us-west-2c']
instanceType = 'p3.16xlarge'
# instanceType = 'p3dn.24xlarge'
instanceCount = 4

while True:
  for az in zones:
    print(az)
    try:
      response = client.create_capacity_reservation(
          InstanceType=instanceType,
          InstancePlatform='Linux/UNIX',
          AvailabilityZone=az,
          InstanceCount=instanceCount,
          EndDateType='unlimited',
      )
      print("Finally found!")
      print(response)
      break
    except ClientError as e:
      if e.response['Error']['Code'] != 'InsufficientInstanceCapacity':
        raise e
  else:
    print ("None available. Retrying in 60 seconds")
    time.sleep(60)

