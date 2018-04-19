# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 21:12:08 2018

@author: G.Poudel
"""

import boto3
import paramiko
import time



def lambda_handler(event, context):

	ec2 = boto3.resource('ec2', region_name='your-ec2-region-name')

	ids = ['your-ec2-instance-id']
	
	#Start an instance
	ec2.instances.filter(InstanceIds=ids).start()

	#Giving some time to start the instance completely 
	time.sleep(60)

	#print few details of the instance
	instances = ec2.instances.filter(InstanceIds=ids)
	for instance in instances:
		print("Instance id - ", instance.id)
		print("Instance public IP - ", instance.public_ip_address)
		print("Instance private IP - ", instance.private_ip_address)
		print("Public dns name - ", instance.public_dns_name)
		print("----------------------------------------------------")
	
	
	
	#connect to S3, we will use it get the pem key file of your ec2 instance
	s3_client = boto3.client('s3')

	#Download private key file from secure S3 bucket and save it inside /tmp/ folder of lambda event
	s3_client.download_file('YourBucketName','YourPEMFileObject.pem', '/tmp/keyname.pem')
 
    #Allowing few seconds for the download to complete
	time.sleep(20)
			
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	privkey = paramiko.RSAKey.from_private_key_file('/tmp/keyname.pem')
	ssh.connect(instance.public_dns_name,username='Your-ec2-UserName',pkey=privkey)  #username --> most likely ec2-user or root or ubuntu depending upon yor ec2 AMI
	stdin, stdout, stderr = ssh.exec_command('echo "ssh to ec2 instance successful"')	
	stdin.flush()
	data = stdout.read().splitlines()
	for line in data:
		print(line)

	ssh.close()


	#Stop an instance
	ec2.instances.filter(InstanceIds=ids).stop()
