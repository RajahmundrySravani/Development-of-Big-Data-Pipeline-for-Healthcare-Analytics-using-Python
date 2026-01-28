from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('MONGO_DB')]

patient = db.patients_processed.find_one()
print("Sample patient data:")
print(f"Gender: {patient.get('gender')}")
print(f"Smoker: {patient.get('smoker_status')}")
print(f"Alcohol: {patient.get('alcohol_use')}")
client.close()
