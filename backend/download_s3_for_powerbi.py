"""
Download Cleaned CSV Files from S3 for Power BI
This script downloads the processed data files for Power BI dashboard creation
"""

import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.getenv('AWS_BUCKET_NAME', 'sravani-healthcare-data')

# Create output directory
output_dir = Path('powerbi_data')
output_dir.mkdir(exist_ok=True)

print("=" * 70)
print("📥 DOWNLOADING S3 FILES FOR POWER BI")
print("=" * 70)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Files to download
files_to_download = [
    ('processed/cleaned/patients_cleaned.csv', 'patients_cleaned.csv'),
    ('processed/cleaned/visits_cleaned.csv', 'visits_cleaned.csv'),
    ('processed/cleaned/prescriptions_cleaned.csv', 'prescriptions_cleaned.csv')
]

print(f"\n📂 Output Directory: {output_dir.absolute()}")
print(f"☁️  S3 Bucket: {AWS_BUCKET}\n")

# Download each file
for s3_key, local_filename in files_to_download:
    try:
        local_path = output_dir / local_filename
        
        print(f"⏬ Downloading {s3_key}...")
        s3_client.download_file(AWS_BUCKET, s3_key, str(local_path))
        
        # Get file size
        file_size = local_path.stat().st_size / 1024  # KB
        
        print(f"   ✅ Saved: {local_filename} ({file_size:.2f} KB)")
        
    except Exception as e:
        print(f"   ❌ Error downloading {s3_key}: {e}")

print("\n" + "=" * 70)
print("✅ DOWNLOAD COMPLETE!")
print("=" * 70)

# List downloaded files
print("\n📋 Downloaded Files:")
for file in output_dir.glob('*.csv'):
    size_kb = file.stat().st_size / 1024
    print(f"   - {file.name} ({size_kb:.2f} KB)")

print("\n💡 Next Steps:")
print("1. Open Power BI Desktop")
print("2. Click 'Get Data' → 'Text/CSV'")
print(f"3. Navigate to: {output_dir.absolute()}")
print("4. Import all 3 CSV files")
print("5. Follow POWER_BI_SETUP.md guide for dashboard creation")

print("\n🔗 Files Location:")
print(f"   {output_dir.absolute()}")
