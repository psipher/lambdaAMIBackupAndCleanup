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

#### 1. SETUP IAM PERMISSIONS
Login to your AWS Management console, Go to Services, and click on **IAM** under Security , Identity & compliance . <br/>
In IAM Dashboard, Go to **Policies** tab, click Create Policy and paste the content of the following JSON in Policy Document, and click on Create Policy

    { "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "logs:*" ], "Resource": "arn:aws:logs:*:*:*" }, { "Effect": "Allow", "Action": "ec2:*", "Resource": "*" } ] }

image 1
You can name the policy as **lamda-ec2-ami-policy**
Now Click on **Roles**, and **Create New Role**. Under _AWS Service Roles_, select _AWS Lambda_ as the _Role Type_ and then proceed to click **Next:Permissions**
Now click on **filter polices** and select **customer managed**
Select the policy you created and click **next :tags** . Tags can be left emptied and select **next:Review**. <br/> You can now create  role with role name as  **lamda-ec2-ami-role**. Click create **role**  <br/>
 
 Here’s the IAM Role (**lamda-ec2-ami-role**) with the attached policy (**lamda-ec2-ami-policy**)
Image
We have just created a role for which we have allowed permissions to EC2 instances and view logs in Cloudwatch.

#### 2. CREATE LAMBDA BACKUP FUNCTION
Now that we have created a role and a policy, we’ll have to create the first function that allows us to backup every instance in our account, which has a **"Backup"** key tag. We don’t have to indicate a value here. <br/>

Here’s how the AMI backup script works:
For **daily backup** , the script will first search for all ec2 instances having a tag with **"BackupDaily**” on it. Similarly it will look for **BackupWeekly** and **BackupMonthly** incase you need to setup weekly and monthly backups too.<br/>
As soon as it has the instances list, it loops through each instance and then creates an AMI of it.
Also, it will look for a **"RetentionDaily"** , **RetentionWeekly** and **RetentionMonthly** tag key which will be used as a retention policy number in days. If there is no tag with that name, it will use a 7 days default value for each AMI.<br/>
 After creating the AMI it creates a **"DeleteOn"** tag on the AMI indicating when it will be deleted using the Retention value and another Lambda function. <br/>
 So here’s how you can create your first function. Go to Services, Lambda, and click Create a Lambda Function: Login to your [AWS Management console](https://console.aws.amazon.com/lambda/), Go to **Services**, and click on **Lambda** under **Compute**. <br/>

1. Click **Create functions** and **select Author from scratch** <br/>
2. Give a name for it - **lambdaAMIBackupsDaily**
3. Select Python 3.8 as a Runtime option.
4. Under **Change default execution role**, select **Use an existing role**
5. Select the previously created IAM role **(lamda-ec2-ami)**
6. Click **Create function**
7. **Now paste the lambdaAMIBackupsDaily code from the repo** under function code.
8. Under the **basic settings** select **timeout** as 1 minute and **Memory** as 256mb in order to avoid memory issues . You can change these according to your requirements.
9. Now create the **lambdaAMIBackupsWeekly** and **lambdaAMIBackupsMonthly** if weekly and monthly ami backups are required using the code in the repo.

#### 3. **CREATE LAMBDA CLEANUP FUNCTION** 
Having successfully created the AMI using the previous function, we need to now remove them when not needed anymore. <br/>
Here’s how the AMI cleanup script works:
The script first searches for all ec2 instances having a tag with **"Backup”** on it. As soon as it has the instances list, it loops through each instance and reference the AMIs of that instance. It checks that the latest daily backup succeeded then it stores every image that's reached its DeleteOn tag's date for deletion. It then loops through the AMIs, de-registers them and removes all the snapshots associated with that AMI.
Using the same steps as before, create the function **lambdaAMICleanupDaily**, **lambdaAMICleanupWeekly** and **lambdaAMICleanupMonthly**   respectively and paste the provided code. <br/>
So, you have now working functions that will backup AMI and remove those when "DeleteOn" specifies. And now, it’s time to automate using the Event sources feature from Lambda.
#### 4. **SCHEDULE FUNCTIONS** 
The function:<br/>
 **lambdaAMIBackupsDaily** : Needs to run atleast once a day from monday to saturday.<br/>
 **lambdaAMIBackupsWeekly** : Needs to be run every Sunday .<br/>
 **lambdaAMICleanupMonthly** : Needs to run first of every month.<br/>
To Schedule functions , go to aws cloudwatch, select **Rules** and **create Rule**
 
 


