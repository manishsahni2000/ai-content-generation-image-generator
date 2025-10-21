from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def add_text_to_image(image_data, message, font_path=None):
    """
    Adds black text with red background at the bottom of the image.
    """
    img = Image.open(BytesIO(image_data))
    draw = ImageDraw.Draw(img)

    # Use a larger font (Heading-like)
    font_size = max(24, int(img.height * 0.05))  # 5% of image height
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    # Measure text size
    text_bbox = draw.textbbox((0, 0), message, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Position text at bottom center
    x = (img.width - text_width) / 2
    y = img.height - text_height - 20  # 20 px from bottom

    # Draw red background rectangle behind text
    padding = 10
    draw.rectangle(
        [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
        fill="red"
    )

    # Draw black text
    draw.text((x, y), message, fill="black", font=font)

    # Save to bytes
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()