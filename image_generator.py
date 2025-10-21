import json, base64, time, random, os
from botocore.exceptions import ClientError
from rekognition_text import create_rekognition_mask, replace_text_with_heading_style

# Rate limiting configuration
RATE_LIMIT_INTERVAL = 30
MAX_RETRIES = 5
INITIAL_BACKOFF = 1
last_request_time = 0


def generate_or_reuse_image(bedrock_client, model_id, prompt, width, height, product, ratio_name, input_assets_dir, brief,output_assets_dir,num):
    """
    Generates or modifies an image:
    - If an existing image is found and brief["text_to_replace"] exists → use Rekognition to modify text.
    - Otherwise, generate a new image using Amazon Titan.
    """
    global last_request_time

    existing_image_path = os.path.join(input_assets_dir, f"{product}_{ratio_name}_1.png")
    # ✅ Case 1: Existing image → Modify or reuse
    if os.path.exists(existing_image_path):
        print(f"Reusing existing asset for {product} [{ratio_name}] → {existing_image_path}")

        # If the brief has text_to_replace, modify the image using Rekognition
        if brief and "text_to_replace" in brief and brief["text_to_replace"].strip():
            print(f"Modifying existing image using Rekognition for text: '{brief['text_to_replace']}'")

            # Detect and modify text
            img, text_boxes = create_rekognition_mask(existing_image_path)
            replace_text_with_heading_style(
                img,
                text_boxes,
                brief["text_to_replace"],
                brief["campaign_message"],
                font_path=None,
                output_assets_dir=os.path.join(output_assets_dir, product, str(num)),
                product = product,
                num=num,
                ratio_name = ratio_name
            )

            # Return modified image bytes
            with open("updated_image_heading2.png", "rb") as f:
                return f.read()

        # Otherwise, just reuse existing image
        with open(existing_image_path, "rb") as f:
            return f.read()

    # ✅ Case 2: No existing image → Generate using Titan
    print(f"Generating new image for {product} [{ratio_name}] ({width}x{height})...")

    seed = random.randint(0, 2147483647)
    native_request = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": prompt},
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "cfgScale": 8.0,
            "height": height,
            "width": width,
            "seed": seed,
        },
    }
    request = json.dumps(native_request)

    # Rate limit enforcement
    current_time = time.time()
    if current_time - last_request_time < RATE_LIMIT_INTERVAL:
        sleep_time = RATE_LIMIT_INTERVAL - (current_time - last_request_time)
        print(f"Rate limiting: Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

    # Retry logic with exponential backoff
    backoff = INITIAL_BACKOFF
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Generating image attempt {attempt + 1}...")
            response = bedrock_client.invoke_model(modelId=model_id, body=request)
            last_request_time = time.time()

            model_response = json.loads(response["body"].read())
            image_data = base64.b64decode(model_response["images"][0])

            # Save generated image for reuse
            os.makedirs(input_assets_dir, exist_ok=True)
            with open(existing_image_path, "wb") as f:
                f.write(image_data)
            print(f"✅ Saved generated image for reuse: {existing_image_path}")

            return image_data

        except ClientError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(backoff)
            backoff *= 2

    return None