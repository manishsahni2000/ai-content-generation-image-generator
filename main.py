import argparse
import os
from clients import initialize_clients
from config import MODEL_ID, ASPECT_RATIOS, INPUT_ASSETS_DIR, OUTPUT_ASSETS_DIR
from brief_loader import load_brief
from prompt_builder import build_prompt
from guardrails_validator import validate_prompt_with_guardrails
from image_generator import generate_or_reuse_image
from image_overlay import add_text_to_image
from storage_manager import upload_and_save_local

def process_product(product, brief, ratio, i, bedrock_client, s3_client):
    prompt = build_prompt(brief, product)
    print(f"Prompt for {product}: {prompt}")
    validate_prompt_with_guardrails(prompt)
    image_data = generate_or_reuse_image(bedrock_client, MODEL_ID, prompt, ratio["width"], ratio["height"],product,ratio["name"],INPUT_ASSETS_DIR,brief,OUTPUT_ASSETS_DIR,i)
    modified = add_text_to_image(image_data, brief["campaign_message"])
    upload_and_save_local(s3_client, product, modified, ratio, i)

def main():
    parser = argparse.ArgumentParser(description="Campaign Image Generation Pipeline")
    parser.add_argument("--brief", required=True, help="Path to campaign brief JSON")
    args = parser.parse_args()

    bedrock_client, s3_client = initialize_clients()
    brief = load_brief(args.brief)

    i = 1
    for product in brief["products"]:
        for ratio in ASPECT_RATIOS:
            process_product(product, brief, ratio, i, bedrock_client, s3_client)

    print("Campaign generation complete.")

if __name__ == "__main__":
    main()