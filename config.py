import os

MODEL_ID = "amazon.titan-image-generator-v1"
BUCKET_NAME = "campaign-poc-images-bucket"
REGION = "us-east-1"

OUTPUT_DIR = "output"
INPUT_ASSETS_DIR = "input_assets"
OUTPUT_ASSETS_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(INPUT_ASSETS_DIR, exist_ok=True)

ASPECT_RATIOS = [
    {"name": "1:1", "width": 768, "height": 768},
    {"name": "16:9", "width": 1152, "height": 640},
    {"name": "9:16", "width": 384, "height": 576},
]