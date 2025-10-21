import os
from botocore.exceptions import ClientError
from config import OUTPUT_DIR, BUCKET_NAME

def upload_and_save_local(s3_client, product, modified_data, ratio, i):
    s3_key = f"images/{product}/{product}_{ratio['name']}_{i}.png"
    try:
        s3_client.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=modified_data, ContentType="image/png")
        print(f"Uploaded: s3://{BUCKET_NAME}/{s3_key}")
    except ClientError as e:
        print(f"S3 upload failed: {e}")
        return False

    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        retrieved = response["Body"].read()
        local_dir = os.path.join(OUTPUT_DIR, product)
        os.makedirs(local_dir, exist_ok=True)
        path = os.path.join(local_dir, f"{product}_{ratio['name']}_{i}.png")
        with open(path, "wb") as f:
            f.write(retrieved)
        print(f"Saved locally: {path}")
        print(f"********************************************************")
        print(f"********************************************************")
        return True
    except ClientError as e:
        print(f"S3 retrieve failed: {e}")
        return False