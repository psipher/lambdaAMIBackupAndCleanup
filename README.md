# lambdaAMIBackups & Cleanup Python 3
Automated AMI Backups using python 3
This Repo conatains AMI daily, weekly and monthly backup scripts.
Why do I need AMI Backups and Cleanups?
AMI makes it easier and faster to recover an instance in case of a disaster or failure of the instance, and therefore, automating this process is the way to go.

The process, generally comprises of the following steps:

Let’s now take a closer look at each of them with some demos and screenshots to make it easier.
1.	Setup IAM Permissions
2.	Create Lambda Backup Function
3.	Create Lambda Cleanup Function
4.	Schedule Functions
5.	 Tagging EC2 Instance

