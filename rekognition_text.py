import boto3
from PIL import Image, ImageDraw, ImageFont
import io

# -------------------------------
# Step 1: Detect text and create mask
# -------------------------------
def create_rekognition_mask(image_path):
    """
    Detects text using Rekognition and creates overlay info.
    """
    rekognition = boto3.client("rekognition", region_name="us-east-1")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = rekognition.detect_text(Image={"Bytes": image_bytes})
    detections = response["TextDetections"]

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = img.size

    # Overlay (debug)
    overlay_img = img.copy()
    draw_overlay = ImageDraw.Draw(overlay_img, "RGBA")

    text_boxes = []

    for det in detections:
        if det["Type"] == "LINE" and "Geometry" in det:
            box = det["Geometry"]["BoundingBox"]
            left = int(box["Left"] * width)
            top = int(box["Top"] * height)
            right = left + int(box["Width"] * width)
            bottom = top + int(box["Height"] * height)

            draw_overlay.rectangle([left, top, right, bottom], fill=(255,0,0,120), outline=(255,0,0,255))

            text_boxes.append({
                "text": det["DetectedText"],
                "bbox": [left, top, right, bottom]
            })

    overlay_path = image_path.replace(".png", "_overlay.png")
    overlay_img.save(overlay_path)
    print(f"Overlay saved → {overlay_path}")

    return img, text_boxes

# -------------------------------
# Step 2: Replace text using PIL
# -------------------------------

def replace_text_with_heading_style(img, text_boxes, text_to_replace, new_text, font_path=None, output_assets_dir=None, product=None, num=None, ratio_name=None):
    """
    Replaces detected text with a Heading-2 style:
    - Black text
    - Red background
    - Larger font
    """
    draw = ImageDraw.Draw(img)

    for tb in text_boxes:
        detected_text = tb["text"].strip()
        if text_to_replace.strip().lower() in detected_text.lower():
            left, top, right, bottom = tb["bbox"]

            # Fill background with red
            draw.rectangle([left, top, right, bottom], fill="red")

            # Determine font size dynamically (big for heading)
            font_size = max(24, int((bottom - top) * 1.2))
            font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

            # Use textbbox to measure text
            bbox = draw.textbbox((0,0), new_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Center text in the box
            x = left + (right - left - text_width) / 2
            y = top + (bottom - top - text_height) / 2

            draw.text((x, y), new_text, fill="black", font=font)
            print(f"Replaced '{detected_text}' with '{new_text}' in Heading-2 style in box {tb['bbox']}")

    img.save(f"{output_assets_dir}_{product}_{ratio_name}_{num}_updated.png")
    print(f"Updated image saved → {output_assets_dir}")
    return output_assets_dir

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    image_path = "input_assets/Protien Shake_1:1.png"
    text_to_replace = "SHAKE"
    new_text = "ADOBE ENERGY !!"

    # Step 1: Detect text
    img, text_boxes = create_rekognition_mask(image_path)

    # Step 2: Replace text
    replace_text_with_heading_style(img, text_boxes, text_to_replace, new_text, font_path=None)