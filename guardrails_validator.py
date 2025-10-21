import boto3
import json
from config import REGION
import sys

def validate_prompt_with_guardrails(prompt):
    client = boto3.client("bedrock-runtime", region_name=REGION)
    guardrail_id = "qvtn789dcl0w"  # replace with yours
    #guardrail_version = "3"
    guardrail_version = "5"

    print(f"Validating prompt with Guardrail {guardrail_id}...")
    response = client.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version,
        source="INPUT",
        content=[{
            "text": {
                "text": prompt
            }
        }],
        outputScope="FULL"
    )

    # Check the action type
    action = response.get("action", "")
    if action == "GUARDRAIL_INTERVENED":
        outputs = response.get("outputs", [])
        if outputs and "text" in outputs[0]:
            message = outputs[0]["text"]
            print(f"Guardrail Message: {message}")
        else:
            print("Guardrail intervened, but no output message found.")
        
        # Stop further processing gracefully
        print("Generation stopped due to Guardrail intervention.")
        sys.exit(0)
    else:
        print("No guardrail intervention detected.")