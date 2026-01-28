"""
Healthcare Data Processing with PySpark
Downloads from S3, processes with PySpark, saves to MongoDB
"""

import os
import sys

# CRITICAL: Set these BEFORE any PySpark imports
os.environ['SPARK_LOCAL_HOSTNAME'] = 'localhost'
os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'
# Tell PySpark to use 'python' instead of 'python3' on Windows
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from dotenv import load_dotenv
load_dotenv()

import boto3
from pymongo import MongoClient

# Now import PySpark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count
from pyspark.sql.types import IntegerType, DoubleType
import shutil

# AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.getenv('AWS_BUCKET_NAME', 'sravani-healthcare-data')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'healthcare_analytics')

print("=" * 70)
print("🚀 HEALTHCARE DATA PROCESSING WITH PYSPARK")
print("=" * 70)

# Step 1: Download CSV files from S3
print("\n📥 Step 1: Downloading CSV files from S3...")
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Create temp directory
temp_dir = "temp_data"
os.makedirs(temp_dir, exist_ok=True)

# Download files from S3
def download_s3_files(prefix):
    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET, Prefix=prefix)
    if 'Contents' not in response:
        return []
    
    files = []
    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith('.csv'):
            filename = os.path.basename(key)
            local_path = os.path.join(temp_dir, filename)
            s3_client.download_file(AWS_BUCKET, key, local_path)
            files.append(local_path)
    return files

patient_files = download_s3_files('raw/patients/')
visit_files = download_s3_files('raw/visits/')
prescription_files = download_s3_files('raw/prescriptions/')

print(f"   ✅ Downloaded {len(patient_files)} patient files")
print(f"   ✅ Downloaded {len(visit_files)} visit files")
print(f"   ✅ Downloaded {len(prescription_files)} prescription files")

# Step 2: Initialize PySpark Session
print("\n📊 Step 2: Initializing PySpark Session...")
spark = SparkSession.builder \
    .appName("HealthcareDataProcessing") \
    .master("local[*]") \
    .config("spark.driver.host", "localhost") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("   ✅ PySpark Session Created!")

# Step 3: Process Patient Data with PySpark
print("\n👥 Step 3: Processing Patient Data with PySpark...")
patients_data = []
try:
    if patient_files:
        # Read CSV files with PySpark
        df_patients = spark.read.csv(patient_files, header=True, inferSchema=True)
        print(f"   📊 Loaded {df_patients.count()} raw patient records")
        
        # Clean and transform with PySpark
        df_patients_clean = df_patients \
            .dropna(subset=['patient_id']) \
            .withColumn('age', col('age').cast(IntegerType())) \
            .withColumn('bmi', col('bmi').cast(DoubleType())) \
            .filter((col('age') >= 0) & (col('age') <= 150))
        
        # Add age group using PySpark when/otherwise
        df_patients_clean = df_patients_clean.withColumn(
            'age_group',
            when(col('age') < 18, '0-17')
            .when(col('age') < 35, '18-34')
            .when(col('age') < 50, '35-49')
            .when(col('age') < 65, '50-64')
            .otherwise('65+')
        )
        
        cleaned_count = df_patients_clean.count()
        print(f"   ✅ Processed {cleaned_count} patient records with PySpark")
        
        # Convert date columns to strings for MongoDB compatibility
        for col_name in df_patients_clean.columns:
            if 'date' in col_name.lower():
                df_patients_clean = df_patients_clean.withColumn(col_name, col(col_name).cast('string'))
        
        # Convert to list for MongoDB
        patients_data = [row.asDict() for row in df_patients_clean.collect()]
    else:
        print("   ⚠️  No patient files found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 4: Process Visit Data with PySpark
print("\n🏥 Step 4: Processing Visit Data with PySpark...")
visits_data = []
try:
    if visit_files:
        # Read CSV files with PySpark
        df_visits = spark.read.csv(visit_files, header=True, inferSchema=True)
        print(f"   📊 Loaded {df_visits.count()} raw visit records")
        
        # Clean and transform with PySpark
        df_visits_clean = df_visits \
            .dropna(subset=['visit_id', 'patient_id']) \
            .withColumn('severity_score', col('severity_score').cast(IntegerType())) \
            .withColumn('length_of_stay', col('length_of_stay').cast(IntegerType()))
        
        cleaned_count = df_visits_clean.count()
        print(f"   ✅ Processed {cleaned_count} visit records with PySpark")
        
        # Convert date columns to strings for MongoDB compatibility
        for col_name in df_visits_clean.columns:
            if 'date' in col_name.lower():
                df_visits_clean = df_visits_clean.withColumn(col_name, col(col_name).cast('string'))
        
        # Convert to list for MongoDB
        visits_data = [row.asDict() for row in df_visits_clean.collect()]
    else:
        print("   ⚠️  No visit files found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 5: Process Prescription Data with PySpark
print("\n💊 Step 5: Processing Prescription Data with PySpark...")
prescriptions_data = []
try:
    if prescription_files:
        # Read CSV files with PySpark
        df_prescriptions = spark.read.csv(prescription_files, header=True, inferSchema=True)
        print(f"   📊 Loaded {df_prescriptions.count()} raw prescription records")
        
        # Clean and transform with PySpark
        df_prescriptions_clean = df_prescriptions \
            .dropna(subset=['prescription_id', 'patient_id', 'visit_id']) \
            .withColumn('quantity', col('quantity').cast(IntegerType())) \
            .withColumn('days_supply', col('days_supply').cast(IntegerType()))
        
        cleaned_count = df_prescriptions_clean.count()
        print(f"   ✅ Processed {cleaned_count} prescription records with PySpark")
        
        # Convert date columns to strings for MongoDB compatibility
        for col_name in df_prescriptions_clean.columns:
            if 'date' in col_name.lower():
                df_prescriptions_clean = df_prescriptions_clean.withColumn(col_name, col(col_name).cast('string'))
        
        # Convert to list for MongoDB
        prescriptions_data = [row.asDict() for row in df_prescriptions_clean.collect()]
    else:
        print("   ⚠️  No prescription files found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 6: Calculate Analytics with PySpark
print("\n📈 Step 6: Calculating Analytics with PySpark...")
analytics = {}

if patients_data:
    # Create DataFrame from processed data
    df_patients_final = spark.createDataFrame(patients_data)
    
    # Age distribution using PySpark groupBy
    age_dist = df_patients_final.groupBy('age_group') \
        .agg(count('*').alias('count')) \
        .orderBy('age_group') \
        .collect()
    analytics['age_distribution'] = [{'age_group': row['age_group'], 'count': row['count']} for row in age_dist]
    print(f"   ✅ Age distribution: {len(age_dist)} groups (PySpark aggregation)")
    
    # Gender distribution using PySpark groupBy
    gender_dist = df_patients_final.groupBy('gender') \
        .agg(count('*').alias('count')) \
        .collect()
    analytics['gender_distribution'] = [{'gender': row['gender'], 'count': row['count']} for row in gender_dist]
    print(f"   ✅ Gender distribution calculated (PySpark aggregation)")

if visits_data:
    # Create DataFrame from processed data
    df_visits_final = spark.createDataFrame(visits_data)
    
    # Disease distribution (top 10) using PySpark
    disease_dist = df_visits_final.groupBy('diagnosis_description') \
        .agg(count('*').alias('count')) \
        .orderBy(col('count').desc()) \
        .limit(10) \
        .collect()
    analytics['disease_distribution'] = [{'disease': row['diagnosis_description'], 'count': row['count']} for row in disease_dist]
    print(f"   ✅ Top 10 diseases calculated (PySpark aggregation)")

# Step 6.5: Save Cleaned Data as CSV to S3 (for analytics - Power BI, reporting)
print("\n📦 Step 6.5: Saving Cleaned Data as CSV to S3...")
try:
    import pandas as pd
    
    # Save patients as CSV
    if patients_data:
        df_patients = pd.DataFrame(patients_data)
        csv_path = os.path.join(temp_dir, 'patients_cleaned.csv')
        df_patients.to_csv(csv_path, index=False)
        
        # Upload to S3
        s3_key = 'processed/cleaned/patients_cleaned.csv'
        s3_client.upload_file(csv_path, AWS_BUCKET, s3_key)
        print(f"   ✅ Uploaded patients_cleaned.csv ({len(patients_data)} records)")
    
    # Save visits as CSV
    if visits_data:
        df_visits = pd.DataFrame(visits_data)
        csv_path = os.path.join(temp_dir, 'visits_cleaned.csv')
        df_visits.to_csv(csv_path, index=False)
        
        s3_key = 'processed/cleaned/visits_cleaned.csv'
        s3_client.upload_file(csv_path, AWS_BUCKET, s3_key)
        print(f"   ✅ Uploaded visits_cleaned.csv ({len(visits_data)} records)")
    
    # Save prescriptions as CSV
    if prescriptions_data:
        df_prescriptions = pd.DataFrame(prescriptions_data)
        csv_path = os.path.join(temp_dir, 'prescriptions_cleaned.csv')
        df_prescriptions.to_csv(csv_path, index=False)
        
        s3_key = 'processed/cleaned/prescriptions_cleaned.csv'
        s3_client.upload_file(csv_path, AWS_BUCKET, s3_key)
        print(f"   ✅ Uploaded prescriptions_cleaned.csv ({len(prescriptions_data)} records)")
    
    print(f"   ✅ Cleaned CSV files ready for Power BI/analytics!")
except Exception as e:
    print(f"   ❌ Error saving CSV files: {e}")

# Step 7: Save to MongoDB
print("\n💾 Step 7: Saving to MongoDB...")
try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    
    # Save processed data
    if patients_data:
        db.patients_processed.delete_many({})
        db.patients_processed.insert_many(patients_data)
        print(f"   ✅ Saved {len(patients_data)} patients to MongoDB")
    
    if visits_data:
        db.visits_processed.delete_many({})
        db.visits_processed.insert_many(visits_data)
        print(f"   ✅ Saved {len(visits_data)} visits to MongoDB")
    
    if prescriptions_data:
        db.prescriptions_processed.delete_many({})
        db.prescriptions_processed.insert_many(prescriptions_data)
        print(f"   ✅ Saved {len(prescriptions_data)} prescriptions to MongoDB")
    
    # Save analytics
    if analytics:
        db.analytics.delete_many({})
        db.analytics.insert_one(analytics)
        print(f"   ✅ Saved analytics to MongoDB")
    
    client.close()
    
except Exception as e:
    print(f"   ❌ Error saving to MongoDB: {e}")

# Cleanup
print("\n🧹 Step 8: Cleaning up...")
shutil.rmtree(temp_dir)
print("   ✅ Temporary files removed")

spark.stop()
print("   ✅ PySpark session stopped")

print("\n" + "=" * 70)
print("✅ PYSPARK PROCESSING COMPLETE!")
print("=" * 70)
print("\nPySpark Operations Performed:")
print("✓ CSV reading with spark.read.csv()")
print("✓ Data cleaning with dropna(), withColumn(), filter()")
print("✓ Transformations with when/otherwise for age groups")
print("✓ Aggregations with groupBy(), count(), orderBy()")
print("\nNext steps:")
print("1. Refresh your Dashboard to see processed data")
print("2. Check MongoDB: patients_processed, visits_processed, prescriptions_processed")
