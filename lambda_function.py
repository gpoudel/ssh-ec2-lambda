# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 21:12:08 2018

@author: G.Poudel
"""

import time
import boto3
import paramiko


def lambda_handler(event, context):

    ec2 = boto3.resource('ec2', region_name='your-ec2-region-name')

    instance_id = 'your-ec2-instance-id'

    instance = ec2.Instance(instance_id)

    # Start the instance
    instance.start()

    # Giving some time to start the instance completely
    time.sleep(60)

    # Print few details of the instance
    print("Instance id - ", instance.id)
    print("Instance public IP - ", instance.public_ip_address)
    print("Instance private IP - ", instance.private_ip_address)
    print("Public dns name - ", instance.public_dns_name)
    print("----------------------------------------------------")

    # Connect to S3, we will use it get the pem key file of your ec2 instance
    s3_client = boto3.client('s3')

    # Download private key file from secure S3 bucket
    # and save it inside /tmp/ folder of lambda event
    s3_client.download_file('YourBucketName', 'YourPEMFileObject.pem',
                            '/tmp/keyname.pem')

    # Allowing few seconds for the download to complete
    time.sleep(20)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file('/tmp/keyname.pem')
    # username is most likely 'ec2-user' or 'root' or 'ubuntu'
    # depending upon yor ec2 AMI
    ssh.connect(
        instance.public_dns_name, username='Your-ec2-UserName', pkey=privkey
    )
    stdin, stdout, stderr = ssh.exec_command(
        'echo "ssh to ec2 instance successful"')
    stdin.flush()
    data = stdout.read().splitlines()
    for line in data:
        print(line)

    ssh.close()

    # Stop the instance
    instance.stop()
