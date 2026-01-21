from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    size = 500
    img = Image.new('RGBA', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle or just simple background
    # Let's make it a purple circle/squaricle background
    # But user wants "Khalif", let's just make a big "K"
    
    # Draw Purple K
    try:
        # Try to use the font we downloaded if available
        font_path = "app/Roboto-Bold.ttf"
        if not os.path.exists(font_path):
             font_path = "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
        
        font = ImageFont.truetype(font_path, 400)
    except:
        font = ImageFont.load_default()

    text = "K"
    
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    # Draw
    draw.text(((size - text_w) / 2, (size - text_h) / 2 - 50), text, fill=(131, 58, 180), font=font)
    
    img.save("app/logo.png")
    print("Logo created at app/logo.png")

if __name__ == "__main__":
    create_logo()
