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

### 1. SETUP IAM PERMISSIONS
Login to your AWS Management console, Go to Services, and click on **IAM** under Security , Identity & compliance .
In IAM Dashboard, Go to **Policies** tab, click Create Policy and select JSON to add the policy (you can name the policy as lamda-ec2-ami-policy).
). 
Paste the content of the following JSON in Policy Document, and click on Create Policy
