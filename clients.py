import boto3
from config import REGION

def initialize_clients():
    bedrock = boto3.client("bedrock-runtime", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)
    return bedrock, s3