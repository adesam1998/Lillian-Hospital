import sys
import boto3
from awsglue.transform import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job 
import pyspark.sql.functions as f
from awsglue.dynamicframe import dynamicFrame 



# Initialize the job, spinning up the engine in AWS and start up the spark session
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Put the directories to specify the source files and destinaton location in focus (or dealing with)
data_clinical_trials = 's3://lilianhosp5/clinical_trial.csv'
data_imaging_results = 's3://lilianhosp5/imaging_results.csv'
data_lab_results = 's3://lilianhosp5/lab_results.csv'
data_medical_records = 's3://lilianhosp5/medical_records.csv'
data_patients_data = 's3://lilianhosp5/patients_data.csv'
data_trial_participants = 's3://lilianhosp5/trial_participants.csv'
output_dir = ''

# To read and convert all data into DynamicFrame
clinical_trials = glueContext.create_dynamic_frame.from_options(
    format_options={'quoteChar': '"', 'withHeader': True, 'seperator': ','}
    , connection_type='s3'
    , format='csv'
    , connection_options={'paths': [data_clinical_trials], 'recurse': True}
    , transformation_ctx='clinical_trials',
)

imaging_results = glueContext.create_dynamic_frame.from_options(
    format_options={'quoteChar': '"', 'withHeader': True, 'seperator': ','}
    , connection_type='s3'
    , format='csv'
    , connection_options={'paths': [data_imaging_results], 'recurse': True}
    , transformation_ctx='imaging_results',
)

lab_results = glueContext.create_dynamic_frame.from_options(
    format_options={'quoteChar': '"', 'withHeader': True, 'seperator': ','}
    , connection_type='s3'
    , format='csv'
    , connection_options={'paths': [data_lab_results], 'recurse': True}
    , transformation_ctx='lab_results',
)

medical_records = glueContext.create_dynamic_frame.from_options(
    format_options={'quoteChar': '"', 'withHeader': True, 'seperator': ','}
    , connection_type='s3'
    , format='csv'
    , connection_options={'paths': [data_medical_records], 'recurse': True}
    , transformation_ctx='medical_records',
)

patients_data = glueContext.create_dynamic_frame.from_options(
    format_options={'quoteChar': '"', 'withHeader': True, 'seperator': ','}
    , connection_type='s3'
    , format='csv'
    , connection_options={'paths': [data_patients_data], 'recurse': True}
    , transformation_ctx='patients_data',
)

trial_participants = glueContext.create_dynamic_frame.from_options(
    format_options={'quoteChar': '"', 'withHeader': True, 'seperator': ','}
    , connection_type='s3'
    , format='csv'
    , connection_options={'paths': [data_trial_participants], 'recurse': True}
    , transformation_ctx='trial_participants',
)

# Applying mapping based on the provided columns into the dataframe to set a correct schema
mapped_clinical_trials = ApplyMapping.apply(
    frame=clinical_trials
    , mappings=[
        ('trial_id', 'string', 'trial_id', 'string')
        , ('trial_name', 'string', 'trial_name', 'string')
        , ('principal_investigator', 'string', 'principal_investigator', 'string')
        , ('start_date', 'string', 'start_date', 'string')
        , ('end_date', 'string', 'end_date', 'string')
        , ('trial_description', 'string', 'trial_description', 'string'),
    ],
    transformation_ctx='mapped_clinical_trials'
)

mapped_imaging_results = ApplyMapping.apply(
    frame=imaging_results
    , mappings=[
        ('result_id', 'string', 'result_id', 'string')
        , ('patient_id', 'string', 'patient_id', 'string')
        , ('imaging_type', 'string', 'imaging_type', 'string')
        , ('imaging_date', 'string', 'imaging_date', 'string')
        , ('image_url', 'string', 'image_url', 'string')
        , ('findings', 'string', 'findings', 'string'),
    ],
    transformation_ctx='mapped_imaging_results'
)

mapped_lab_results = ApplyMapping.apply(
    frame=lab_results
    , mappings=[
        ('result_id', 'string', 'result_id', 'string')
        , ('patient_id', 'string', 'patient_id', 'string')
        , ('test_name', 'string', 'test_name', 'string')
        , ('test_date', 'string', 'test_date', 'string')
        , ('test_result', 'string', 'test_result', 'string')
        , ('reference_range', 'string', 'reference_range', 'string'),
    ],
    transformation_ctx='mapped_lab_results'
)

mapped_medical_records = ApplyMapping.apply(
    frame=medical_records
    , mappings=[
        ('record_id', 'string', 'record_id', 'string')
        , ('patient_id', 'string', 'patient_id', 'string')
        , ('admission_date', 'string', 'admission_date', 'string')
        , ('discharge_date', 'string', 'discharge_date', 'string')
        , ('diagnosis', 'string', 'diagnosis', 'string')
        , ('treatment_description', 'string', 'treatment_description', 'string'),
    ],
    transformation_ctx='mapped_medical_records'
)

mapped_patients_data = ApplyMapping.apply(
    frame=patients_data
    , mappings=[
        ('patient_id', 'string', 'patient_id', 'string')
        , ('first_name', 'string', 'first_name', 'string')
        , ('last_name', 'string', 'last_name', 'string')
        , ('date_of_birth', 'string', 'date_of_birth', 'string')
        , ('gender', 'string', 'gender', 'string')
        , ('ethnicity', 'string', 'ethnicity', 'string')
        , ('address', 'string', 'address', 'string')
        , ('contact_number', 'string', 'contact_number', 'string'),
    ],
    transformation_ctx='mapped_patients_data'
)

mapped_trial_participants = ApplyMapping.apply(
    frame=trial_participants
    , mappings=[
        ('participant_id', 'string', 'participant_id', 'string')
        , ('trial_id', 'string', 'trial_id', 'string')
        , ('patient_id', 'string', 'patient_id', 'string')
        , ('enrollment_date', 'string', 'enrollment_date', 'string')
        , ('participant_status', 'string', 'participant_status', 'string'),
    ],
    transformation_ctx='mapped_trial_participants'
)
                                    ## CLEANING AND TRANSFORMATION

# Convert to DataFrame for cleaning and transformation
clinical_trials_df = mapped_clinical_trials.toDF()
imaging_results_df = mapped_imaging_results.toDF()
lab_results_df = mapped_lab_results.toDF()
medical_records_df = mapped_medical_records.toDF()
patients_data_df = mapped_patients_data.toDF()
trial_participants_df = mapped_trial_participants.toDF()

# Transformation