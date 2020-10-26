# Automated AMI BackupDailys
# This code has been updated from python 2 to python 3.8 by Raghav Bhandari
#https://github.com/psipher/lambdaAMIBackupAndCleanup/edit/master/LambdaAMIBackupsDaily.py
# This code has been refered from : https://gist.github.com/bkozora/724e01903a9ad481d21e
#
# This script will search for all instances having a tag with "BackupDaily" 
# on it and are in 'running' state. As soon as it has the instances list, it loop through each instance
# and create an AMI of it. Also, it will look for a "RetentionDaily" tag key which
# will be used as a retention policy number in days. If there is no tag with
# that name, it will use a 4 days default value for each AMI.If there is no tag with that name, it will use a 7 days default value for each AMI.
#
# After creating the AMI it creates a "DeleteOn" tag on the AMI indicating when
# it will be deleted using the RetentionDaily value and another Lambda function 
 

import boto3
import collections
import datetime 

#Specify the region in which EC2 Instances located and to create AMI's. Ex: Mumbai region (us-east-2)
ec = boto3.client('ec2', 'us-east-2')
#ec = boto3.client('ec2')

def lambda_handler(event, context):
    
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['BackupDaily']},
            { 'Name': 'instance-state-name','Values': ['running'] }
        ]
         ).get(
        'Reservations', []
    )
    
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    print("Found %d instances that need backing up" % len(instances))
   
    
    to_tag = collections.defaultdict(list)

    for instance in instances:
        print("Instance name:" + [res['Value'] for res in instance['Tags'] if res['Key'] == 'Name'][0])
        
        #Default retention for 7 days if the tag is not specified
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'RetentionDaily'][0]
        except IndexError:
            retention_days = 7
        except ValueError:
            retention_days = 7
        except Exception as e:    
            retention_days = 7
        
        finally:
        
            create_time = datetime.datetime.now()
            #create_fmt = create_time.strftime('%d-%m-%Y.%H.%M.%S')
            #create_fmt = create_time.strftime('%d-%m-%Y')
            create_fmt = create_time.strftime('%H-%M-%S(UTC)--on--%Y-%m-%d')
    
            try:
                #Check for instance in running state
               # if(ec.describe_instance_status(InstanceIds=[instance['InstanceId']],Filters=[{ 'Name': 'instance-state-name','Values': ['running'] }])['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'):    
                    
                #To make sure instance NoReboot enabled and to name the AMI
                
                AMIid = ec.create_image(InstanceId=instance['InstanceId'], Name="Lambda -Daily " + [result['Value'] for result in instance['Tags'] if result['Key'] == 'Name'][0] + " - " + " From " + create_fmt, Description="Lambda created AMI of instance " + instance['InstanceId'], NoReboot=True, DryRun=False)
                to_tag[retention_days].append(AMIid['ImageId'])

                print("Retaining AMI %s of instance %s for %d days" % (
                        AMIid['ImageId'],
                        instance['InstanceId'],
                        retention_days,
                    ))
        
        
                for retention_days in list(to_tag.keys()):
                    delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
                    delete_fmt = delete_date.strftime('%d-%m-%Y')
                    print("Will delete %d AMIs on %s" % (len(to_tag[retention_days]), delete_fmt))
                    
                    #To create a tag to an AMI when it can be deleted after retention period expires
                    ec.create_tags(
                        Resources=to_tag[retention_days],
                        Tags=[
                            {'Key': 'DeleteOn', 'Value': delete_fmt},
                            ]
                        )
            #If the instance is not in running state        
            except IndexError as e:
                print("Unexpected error, instance "+[res['Value'] for res in instance['Tags'] if res['Key'] == 'Name'][0]+"-"+"\""+instance['InstanceId']+"\""+" might be in the state other then 'running'. So, AMI creation skipped.")    
