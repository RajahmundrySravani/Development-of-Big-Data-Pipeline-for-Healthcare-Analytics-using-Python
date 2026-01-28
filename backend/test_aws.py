from dotenv import load_dotenv
import os
import boto3

# Load .env file
load_dotenv()

# Get credentials
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('AWS_BUCKET_NAME')
region = os.getenv('AWS_REGION')

print("=" * 50)
print("Testing AWS Credentials")
print("=" * 50)
print(f"Access Key: {access_key}")
print(f"Secret Key: {secret_key[:10]}..." if secret_key else "None")
print(f"Bucket: {bucket_name}")
print(f"Region: {region}")
print("=" * 50)

# Test S3 connection
try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    
    # Try to list bucket
    response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
    print("✅ SUCCESS! AWS credentials are working!")
    print(f"✅ Bucket '{bucket_name}' is accessible!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\n💡 Solution: Wait 2-3 minutes and try again, or create new access keys in IAM")
