# ssh-ec2-lambda
#### An AWS lambda function to start, ssh and stop an ec2 instance with python.


### Introduction
Love serverless and aws lambda but I had to do this out of necessity as aws lambdas are still programmable in only few programming languages. Also, to be fair, they are designed to be used for jobs that are quicker (few seconds to few minutes). I needed to run scripts which are not natively supported in lambda and jobs which might run for a little longer. I have been using EC2 intances to generate some reports daily - the jobs typically last few minutes and I have no other reson to keep the instances running otherwise. Because I could also use ssh bash commands to run those scripts, I decided to put everything together in one aws lambda. This lambda function does the following:

* Starts an existing ec2 instance
* Runs ssh commands 
* Stops the ec2 instance 

Depending on how long the instance is going to run, if more than few minutes, stopping the instance can also be done by a seperate lambda after some delay or some other trigger (like the report generated is saved to S3 bucket which then can trigger the Stop ec2 lambda).


### How to use
The Zip is complete and the only thing needed for this purpose. Built under "Amazon Linux AMI ec2 instance" and python3.6 virtualenv. The packages added are 'Request' and 'Paramiko'. Just modify the 'lambda_function.py' inside the zip as per your requirements.


### Requirements




