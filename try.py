import pandas as pd
import boto3
import s3fs
import sys
#from awsglue.transform import *
#from awsglue.utils import getResolvedOptions
#from pyspark.context import SparkContext
#from awsglue.context import GlueContext
#from awsglue.job import Job 
#import pyspark.sql.functions as f
#from awsglue.dynamicframe import dynamicFrame 
import os
import logging
import configparser
import csv


# Reading the configuration .env file
config = configparser.ConfigParser()        # To manage the API keys that want to be keep out of public
config.read('.env')         # To read the private API keys 

access_key=config['AWS']['access_key']             # Acessing the access_key 
secret_key=config['AWS']['secret_key']             # Accessing the secret_key 
bucket_name=config['AWS']['bucket_name']                 # Accessing the S3 bucket name
region=config['AWS']['region']                           # Accessing the nearest region to the data

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
create_bucket()
print(f'{bucket_name} is now available on your AWS account')

                                ##  UPLOAD RAW DATA FROM LOCAL STORAGE TO AWS S3 BUCKET

def upload_to_s3_bucket(dataframes, bucket_name):       # Upload lilian hospital dataframe to AWS S3 bucket
    upload_s3_client = boto3.client(                    # Initialize and connect to AWS S3 bucket through boto3
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    for name, df in dataframes.items():
        try:
            csv_buffer = df.to_csv(index=False)     
            # Uploading the CSV files to S3 bucket         
            upload_s3_client.put_object(Body=csv_buffer, Bucket=bucket_name, Key=f'{name}.csv')
            print(f'File {name} is uploaded successfully to {bucket_name}')
        except Exception as e:
            print(f'Error in uploading {name}.csv to {bucket_name}: {str(e)}')
            
# The main function
if __name__ == '__main__':
    
    # Reading CSV files to DataFrame
    dataframes ={
        'clinical_trial': df_clinical_trial
        , 'imaging_results': df_imaging_results
        , 'lab_results': df_lab_results
        , 'medical_records': df_medical_records
        , 'patients_data': df_patients_data
        , 'trial_participants': df_trial_participants
    }

# Upload the DataFrames to the S3 bucket
upload_to_s3_bucket(dataframes, bucket_name)