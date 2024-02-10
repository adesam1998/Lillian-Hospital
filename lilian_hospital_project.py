import pandas as pd
import boto3
import s3fs
import os
import logging
import configparser
import csv



config = configparser.ConfigParser()        # To manage the API keys that want to be keep out of public
config.read('.env')         # To read the private API keys 

access_key=config['AWS']['access_key']             # Acessing the access_key 
secret_key=config['AWS']['secret_key']             # Accessing the secret_key 
bucket_name=['AWS']['bucket_name']                 # Accessing the S3 bucket name
region=['AWS']['region']                           # Accessing the nearest region to the data

                        ## CREATING THE S3 BUCKET REFERING TO AS DATA LAKE
def create_bucket():
    client = boto3.client(              # Initialize and connect to AWS S3 bucket through boto3
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    client.create_bucket(               # Creating AWS S3 bucket      
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region,
        },
    )

                                ##  UPLOAD RAW DATA FROM LOCAL STORAGE TO AWS S3 BUCKET

def upload_to_s3_bucket(file_paths, bucket_name):       # Upload lilian hospital data to AWS S3 bucket
    upload_s3_client = boto3.client(                    # Initialize and connect to AWS S3 bucket through boto3
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    for file_path in file_paths:
        try:
            object_name = file_path.split('/')[-1]              # Extracting file name for the object name
            upload_s3_client.upload_file(file_path, bucket_name, object_name)
            print(f'File {file_path} is uploaded successfully to {bucket_name}')
        except:
            print(f'Error in uploading {file_path} to {bucket_name}')

file_paths =[
    clinical_trial=['files']['clinical_trial']
    , imaging_result=['files']['df_imaging_result']
    , lab_results=['files']['lab_results']
    , medical_records=['files']['medical_records']
    , patients_data=['files']['patients_data']
    , trial_participants=['files']['trial_participants']
]
                                