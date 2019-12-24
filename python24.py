import boto3
from botocore.client import ClientError
import sys
import argparse
assume_Role = boto3.client('sts',region_name='ap-south-1')
#print('Default Provider Identity: : ' + assume_Role.get_caller_identity()['Arn'])
assume_Role_Arn = 'arn:aws:iam::434662252123:role/shared-lifestyle-jenkins-assumable-role'
assume_Role_Session_Name = 'stage'
response=assume_Role.assume_role (
    RoleArn=assume_Role_Arn,
    RoleSessionName=assume_Role_Session_Name
) 
creds=response['Credentials']
sts_assumed_role = boto3.client('sts',
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken'],
)
# print('AssumedRole Identity: ' + sts_assumed_role.get_caller_identity()['Arn'])
ec2=boto3.client(
    'ec2',
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken'],
)
args = sys.argv
def desc_ec2(*args):
    describe_ec2 = ec2.describe_instances(
    InstanceIds= [*args[1:]]
    )
    return describe_ec2
describe_ec2_status=desc_ec2(*args)
for i in range (0, len(args)-1):
    if(describe_ec2_status['Reservations'][i]['Instances'][0]['State']['Name'] == 'running'):
        print('Now Stopping the instances' + '::::' + str([(describe_ec2_status['Reservations'][i]['Instances'][0]['InstanceId'])]))   
        stop_ec2 = ec2.stop_instances(
            InstanceIds= [(describe_ec2_status['Reservations'][i]['Instances'][0]['InstanceId'])]
        )
    elif(describe_ec2_status['Reservations'][i]['Instances'][0]['State']['Name'] == 'stopped'):
        print('Now starting the instances'+ '::::' + str([(describe_ec2_status['Reservations'][i]['Instances'][0]['InstanceId'])]))
        start_ec2 = ec2.start_instances(
            InstanceIds= [(describe_ec2_status['Reservations'][i]['Instances'][0]['InstanceId'])]
        )    
    else:
        print('Instance is not exist or Terminated')
