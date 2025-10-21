# Creative Automation Pipeline (Amazon Bedrock Titan)

This **Proof-of-Concept (PoC)** demonstrates an **end-to-end automated workflow** for generating **marketing campaign images** using **Amazon Bedrock’s Titan Image Generator**.  
The solution supports **dynamic prompt generation**, **AWS Bedrock Guardrails validation**, **text overlays**, **rate limiting**, and **S3 synchronization** — all fully modularized for scalability and reuse.

---

##  Key Features

- 🧩 **Dynamic Prompt Construction** based on campaign brief JSON  
- 🧠 **AWS Bedrock Titan Image Generator (v1)** for creative generation  
- 🛡️ **Integrated Guardrails Validation** to enforce content safety  
- ⚡ **Optional Local Asset Reuse** for faster re-runs  
- 🖋️ **Custom Text Overlays** using Pillow (PIL)  
- ☁️ **Automatic Upload and Retrieval** from Amazon S3  
- 📐 **Configurable Aspect Ratios** for multiple creative dimensions  
- ⏱️ **Rate Limiting & Exponential Backoff** for API compliance  
- 🧱 **Modular Python Structure** for maintainability and unit testing  

---

## Architecture Overview

```ImageGenerationRag/
│
├── main.py                  # Entry point
├── config.py                # Global configuration (S3 bucket, model ID, etc.)
├── clients.py               # AWS client initialization
├── brief_loader.py          # Load and validate campaign brief
├── prompt_builder.py        # Build dynamic prompts from JSON template
├── guardrails_validator.py  # Validate prompts via Amazon Bedrock Guardrail
├── image_generator.py       # Image generation (Titan + rate limiting)
├── image_overlay.py         # Add campaign message as text overlay
├── storage_manager.py       # S3 upload/download and local storage```
```
---

## 🧾 Example Campaign Brief

**File:** `campaign_brief.json`
```json
{
    "products": ["Murder Scene","Mango Shake"],
    "target_region": "Australia",
    "target_audience": "Young Adults",
    "campaign_message": "ADOBE ENERGY !!",
    "text_to_replace": "SHAKE",
    "prompt_template": "A marketing image of {product} targeted at {target_audience} in {target_region}'."
}
```

## Prompt Template Variables

Variable
Description
{product}
Product name from the list
{target_region}
Campaign region
{target_audience}
Intended audience
{campaign_message}
Marketing slogan or message

## Setup Instructions

```
git clone <repo-url>
cd ImageGenerationRag
pip install -r requirements.txt
```

## Configure AWS Credentials
You must have the following AWS permissions:
	•	bedrock:InvokeModel
	•	bedrock:ApplyGuardrail
	•	s3:PutObject, s3:GetObject

## Set credentials using either:
```
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=us-east-1
```

## Enable Amazon Titan
•	Navigate to AWS Bedrock Console
•	Enable Amazon Titan Image Generator v1 for your account and region

## Create Required Directories
```mkdir input_assets output```

## How to Run

```python main.py --brief campaign_brief.json```

The script will:
	1.	Load the campaign brief
	2.	Dynamically build prompts
	3.	Validate prompts using Bedrock Guardrails
	4.	Generate creative images (reuse local assets if available)
	5.	Add campaign text overlays
	6.	Upload results to S3 and save locally

## Local Output:

output/{product}/

## S3 Upload Path:

```s3://<your-bucket>/images/{product}/...```

## Example Console Log

Prompt for Protien Shake: A marketing image of Protien Shake targeted at Young Adults in Australia'.
Validating prompt with Guardrail qvtn789dcl0w...
No guardrail intervention detected.
Generating new image for Protien Shake [16:9] (1152x640)...
Generating image attempt 1...
✅ Saved generated image for reuse: input_assets/Protien Shake_16:9_1.png
Uploaded: s3://campaign-poc-images-bucket/images/Protien Shake/Protien Shake_16:9_1.png
Saved locally: output/Protien Shake/Protien Shake_16:9_1.png

## Resulting Directory Structure

```
output/
└── Protein Shakes/
    ├── Protein Shakes_1:1_1.png
    ├── Protein Shakes_16:9_1.png
    └── Protein Shakes_9:16_1.png
```
## Assumptions & Limitations

1.	Default AWS Region is us-east-1 (modify if required).
2.	English-only campaign messages (no localization).
3.	Output files overwrite on name conflict — consider timestamps for production.
4.	Amazon Titan Image Generator v1/v2 does not support text overlay rendering natively; overlays are added using Pillow (PIL.ImageDraw).
5.	Titan does not natively support 9:16 aspect ratio; closest used is 3:2 (384x576).

