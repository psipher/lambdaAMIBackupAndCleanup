Diffchecker logo
Diffchecker


Text


Images


PDF


Excel


Folders
CLI
Desktop App
Sign in
Create an account
Saved Diffs
You must be signed in to save diffs
Sign In
Diff history
a minute ago
Clear
Diff history is cleared on refresh
SplitUnified
WordCharacter
Tools
-11 Removals+11 Additions
# Automated AMI BackupDailys
# This code refered with slight changes: https://gist.github.com/bkozora/724e01903a9ad481d21e
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
#By the time I used this script, the Lamda is not available in Mumbai region. So, I chosen Singapore region.
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
Editor
Clear
Save DiffShare
No file chosenOriginal Text
78
                        instance['InstanceId'],
79
                        retention_days,
80
                    )
81
        
82
        
83
                for retention_days in to_tag.keys():
84
                    delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
85
                    delete_fmt = delete_date.strftime('%d-%m-%Y')
86
                    print "Will delete %d AMIs on %s" % (len(to_tag[retention_days]), delete_fmt)
87
                    
88
                    #To create a tag to an AMI when it can be deleted after retention period expires
89
                    ec.create_tags(
90
                        Resources=to_tag[retention_days],
91
                        Tags=[
92
                            {'Key': 'DeleteOn', 'Value': delete_fmt},
93
                            ]
94
                        )
95
            #If the instance is not in running state        
96
            except IndexError as e:
97
                print "Unexpected error, instance "+[res['Value'] for res in instance['Tags'] if res['Key'] == 'Name'][0]+"-"+"\""+instance['InstanceId']+"\""+" might be in the state other then 'running'. So, AMI creation skipped."    
No file chosenChanged Text
81
        
82
        
83
                for retention_days in list(to_tag.keys()):
84
                    delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
85
                    delete_fmt = delete_date.strftime('%d-%m-%Y')
86
                    print("Will delete %d AMIs on %s" % (len(to_tag[retention_days]), delete_fmt))
87
                    
88
                    #To create a tag to an AMI when it can be deleted after retention period expires
89
                    ec.create_tags(
90
                        Resources=to_tag[retention_days],
91
                        Tags=[
92
                            {'Key': 'DeleteOn', 'Value': delete_fmt},
93
                            ]
94
                        )
95
            #If the instance is not in running state        
96
            except IndexError as e:
97
                print("Unexpected error, instance "+[res['Value'] for res in instance['Tags'] if res['Key'] == 'Name'][0]+"-"+"\""+instance['InstanceId']+"\""+" might be in the state other then 'running'. So, AMI creation skipped.")    

Diffchecker Desktop
Run Diffchecker offline, on your computer, with more features!
CHECK IT OUT

Bibcitation
By Diffchecker: A free online tool to generate citations, reference lists, and bibliographies. APA, MLA, Chicago, and more.
CHECK IT OUT
Find Difference
© 2020 Checker Software Inc.ContactTermsPrivacy Policy
