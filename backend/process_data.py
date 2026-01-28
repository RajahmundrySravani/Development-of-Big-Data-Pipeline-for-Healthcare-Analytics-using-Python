"""
Healthcare Data Processing - Downloads from S3, processes with Pandas, saves to MongoDB
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import boto3
import pandas as pd
from io import StringIO

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.getenv('AWS_BUCKET_NAME', 'sravani-healthcare-data')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'healthcare_analytics')

print("=" * 70)
print("🚀 HEALTHCARE DATA PROCESSING")
print("=" * 70)

# Step 1: Download and Read CSV files from S3
print("\n📥 Step 1: Reading CSV files from S3...")
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Read files directly from S3 into pandas
def read_s3_csvs(prefix):
    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET, Prefix=prefix)
    if 'Contents' not in response:
        return pd.DataFrame()
    
    dfs = []
    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith('.csv'):
            csv_obj = s3_client.get_object(Bucket=AWS_BUCKET, Key=key)
            df = pd.read_csv(StringIO(csv_obj['Body'].read().decode('utf-8')))
            dfs.append(df)
    
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()

patients_df = read_s3_csvs('raw/patients/')
visits_df = read_s3_csvs('raw/visits/')
prescriptions_df = read_s3_csvs('raw/prescriptions/')

print(f"   ✅ Loaded {len(patients_df)} patient records")
print(f"   ✅ Loaded {len(visits_df)} visit records")
print(f"   ✅ Loaded {len(prescriptions_df)} prescription records")

# Step 2: Process Patient Data
print("\n👥 Step 2: Processing Patient Data...")
patients_data = []
try:
    if not patients_df.empty:
        # Clean data
        patients_clean = patients_df.dropna(subset=['patient_id'])
        patients_clean['age'] = pd.to_numeric(patients_clean['age'], errors='coerce')
        patients_clean['bmi'] = pd.to_numeric(patients_clean['bmi'], errors='coerce')
        patients_clean = patients_clean[(patients_clean['age'] >= 0) & (patients_clean['age'] <= 150)]
        
        # Add age group
        def get_age_group(age):
            if age < 18: return '0-17'
            elif age < 35: return '18-34'
            elif age < 50: return '35-49'
            elif age < 65: return '50-64'
            else: return '65+'
        
        patients_clean['age_group'] = patients_clean['age'].apply(get_age_group)
        
        # Convert to dict for MongoDB
        patients_data = patients_clean.to_dict('records')
        print(f"   ✅ Processed {len(patients_data)} patient records")
    else:
        print("   ⚠️  No patient data found")
except Exception as e:
    print(f"   ❌ Error processing patients: {e}")

# Step 3: Process Visit Data
print("\n🏥 Step 3: Processing Visit Data...")
visits_data = []
try:
    if not visits_df.empty:
        # Clean data
        visits_clean = visits_df.dropna(subset=['visit_id', 'patient_id'])
        visits_clean['severity_score'] = pd.to_numeric(visits_clean['severity_score'], errors='coerce')
        visits_clean['length_of_stay'] = pd.to_numeric(visits_clean['length_of_stay'], errors='coerce')
        
        # Convert to dict for MongoDB
        visits_data = visits_clean.to_dict('records')
        print(f"   ✅ Processed {len(visits_data)} visit records")
    else:
        print("   ⚠️  No visit data found")
except Exception as e:
    print(f"   ❌ Error processing visits: {e}")

# Step 4: Process Prescription Data
print("\n💊 Step 4: Processing Prescription Data...")
prescriptions_data = []
try:
    if not prescriptions_df.empty:
        # Clean data
        prescriptions_clean = prescriptions_df.dropna(subset=['prescription_id', 'patient_id', 'visit_id'])
        prescriptions_clean['quantity'] = pd.to_numeric(prescriptions_clean['quantity'], errors='coerce')
        prescriptions_clean['days_supply'] = pd.to_numeric(prescriptions_clean['days_supply'], errors='coerce')
        
        # Convert to dict for MongoDB
        prescriptions_data = prescriptions_clean.to_dict('records')
        print(f"   ✅ Processed {len(prescriptions_data)} prescription records")
    else:
        print("   ⚠️  No prescription data found")
except Exception as e:
    print(f"   ❌ Error processing prescriptions: {e}")

# Step 5: Calculate Analytics
print("\n📈 Step 5: Calculating Analytics...")
analytics = {}

if patients_data:
    patients_clean_df = pd.DataFrame(patients_data)
    
    # Age distribution
    age_dist = patients_clean_df['age_group'].value_counts().to_dict()
    analytics['age_distribution'] = [{'age_group': k, 'count': int(v)} for k, v in age_dist.items()]
    print(f"   ✅ Age distribution: {len(age_dist)} groups")
    
    # Gender distribution
    gender_dist = patients_clean_df['gender'].value_counts().to_dict()
    analytics['gender_distribution'] = [{'gender': k, 'count': int(v)} for k, v in gender_dist.items()]
    print(f"   ✅ Gender distribution calculated")

if visits_data:
    visits_clean_df = pd.DataFrame(visits_data)
    
    # Disease distribution (top 10)
    disease_dist = visits_clean_df['diagnosis_description'].value_counts().head(10).to_dict()
    analytics['disease_distribution'] = [{'disease': k, 'count': int(v)} for k, v in disease_dist.items()]
    print(f"   ✅ Top 10 diseases calculated")

# Step 6: Save to MongoDB
print("\n💾 Step 6: Saving to MongoDB...")
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

print("\n" + "=" * 70)
print("✅ PROCESSING COMPLETE!")
print("=" * 70)
print("\nNext steps:")
print("1. Refresh your Dashboard to see the processed data")
print("2. Check MongoDB collections: patients_processed, visits_processed, prescriptions_processed")
print("3. View analytics in the analytics collection")
