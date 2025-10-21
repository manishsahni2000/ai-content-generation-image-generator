# 🧠 Creative Automation Pipeline (Amazon Bedrock Titan)

This **proof-of-concept (PoC)** demonstrates an end-to-end automated workflow for generating **marketing campaign images** using **Amazon Bedrock’s Titan Image Generator**.  
It supports **dynamic prompt generation**, **AWS Bedrock Guardrails validation**, **text overlays**, **rate limiting**, and **S3 synchronization** — all fully modularized for scalability and reuse.

---

## Features

- **Dynamic prompt construction** based on campaign brief JSON  
- **AWS Bedrock Titan Image Generator** (v1) for creative generation  
- **Integrated Guardrails validation** to enforce content safety before generation  
- **Optional local asset reuse** for faster runs  
- **Custom text overlays** using Pillow  
- **Automatic upload and retrieval** from Amazon S3  
- **Configurable aspect ratios** for multiple creative dimensions  
- **Rate limiting and exponential backoff** to respect API limits  
- **Modular Python structure** for maintainability and unit testing  

---

## 🧩 Architecture Overview

ImageGenerationRag/
│
├── main.py                           # Entry point
├── config.py                         # Global configuration (S3 bucket, model ID, etc.)
├── clients.py                        # AWS client initialization
├── brief_loader.py                   # Load and validate campaign brief
├── prompt_builder.py                 # Build dynamic prompts from JSON template
├── guardrails_validator.py           # Validate prompt via Amazon Bedrock Guardrail
├── image_generator.py                # Image generation (Titan model + rate limiting)
├── image_overlay.py                  # Add campaign message text overlay
├── storage_manager.py                # S3 upload/download and local save

---

## 🧾 Example Campaign Brief

`campaign_brief.json`
```json
{
  "products": ["Protein Shakes", "Fruit Juice"],
  "target_region": "Australia",
  "target_audience": "Young Adults",
  "campaign_message": "Have more power and energy!",
  "prompt_template": "A marketing image of {product} targeted at {target_audience} in {target_region}, conveying the message: '{campaign_message}'."
}

Prompt Template Variables
	•	{product} → Product name from the list
	•	{target_region} → Campaign region
	•	{target_audience} → Intended audience
	•	{campaign_message} → Marketing slogan/message

Setup Instructions

1. Clone and install dependencies

cd ImageGenerationRag
pip install -r requirements.txt

2. Configure AWS credentials

You must have permissions for:
	•	bedrock:InvokeModel
	•	bedrock:ApplyGuardrail
	•	s3:PutObject, s3:GetObject

Set credentials either via:

aws configure

or environment variables:

export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=us-east-1

3. Enable Amazon Titan
	•	Go to AWS Bedrock Console
	•	Enable Amazon Titan Image Generator v1 for your account and region
4. Create the required directories
mkdir input_assets output

5. Prepare your campaign brief
Use the JSON format shown above.

How to Run

Run the complete pipeline

python main.py --brief campaign_brief.json

The script will:
	1.	Load the brief
	2.	Build prompts dynamically
	3.	Validate each prompt with Bedrock Guardrails
	4.	Generate creative images (reusing local assets if found)
	5.	Add text overlays (campaign message)
	6.	Upload to S3 and store locally

Output
	•	Local output under: output/{product}/
	•	Uploaded S3 path: s3://<your-bucket>/images/{product}/...

Example Output

Prompt for Protien Shakes: A marketing image of Protien Shakes targeted at Young Adults in Australia, conveying the message: 'Have more power and Energy'.
Validating prompt with Guardrail qvtn789dcl0w...
Prompt passed guardrail validation.
Generating new image for Protien Shakes [9:16] (384x576)...
Generating image attempt 1...
 Saved generated image for reuse: input_assets/Protien Shakes_9:16.png
Uploaded: s3://campaign-poc-images-bucket/images/Protien Shakes/Protien Shakes_9:16_1.png
Saved locally: output/Protien Shakes/Protien Shakes_9:16_1.png

Resulting directory structure:

output/
└── Protein Shakes/
    ├── Protein Shakes_1:1_1.png
    ├── Protein Shakes_16:9_1.png
    └── Protein Shakes_9:16_1.png

# Assumptions and Limitations

1. Assumes AWS region us-east-1; adjust if needed.
2. English message only (no localization).
3. Overwrites output files if numbering conflicts (add timestamps if needed).
4. Amazon Titan Image Generator (v1 and v2) does not natively support text overlay rendering (i.e., placing custom text directly onto the generated image like “Happy Birthday” or “Sale 50% Off”); I have used Pillow (PIL.ImageDraw) to draw text on Titan output.
5.This model does not have a 9:16 aspect ratio; the closest used is 3:2 (384x576).



