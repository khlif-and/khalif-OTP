import base64
import io
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

class QRGenerator:
    @staticmethod
    def generate_stylized_qr(data: str) -> str:
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        matrix = qr.get_matrix()
        q_size = len(matrix)
        box_size = 20
        border = 4
        img_size = (q_size + 2 * border) * box_size
        
        mask = Image.new("L", (img_size, img_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        for r in range(q_size):
            for c in range(q_size):
                if matrix[r][c] and not QRGenerator._is_finder_pattern(r, c, q_size):
                    x = (c + border) * box_size
                    y = (r + border) * box_size
                    pad = box_size * 0.1
                    mask_draw.ellipse(
                        [x + pad, y + pad, x + box_size - pad, y + box_size - pad], 
                        fill=255
                    )
        
        QRGenerator._draw_finder_patterns(mask_draw, box_size, border, q_size)

        gradient = QRGenerator._create_gradient(img_size)
        
        final_img = Image.new("RGBA", (img_size, img_size), "white")
        final_img.paste(gradient, (0, 0), mask)
        
        QRGenerator._embed_logo(final_img, img_size)
        
        buffered = io.BytesIO()
        final_img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    @staticmethod
    def _is_finder_pattern(r, c, q_size) -> bool:
        if r < 7 and c < 7: return True
        if r < 7 and c >= q_size - 7: return True
        if r >= q_size - 7 and c < 7: return True
        return False

    @staticmethod
    def _draw_finder_patterns(draw, box_size, border, q_size):
        def draw_one(r_start, c_start):
            x = (c_start + border) * box_size
            y = (r_start + border) * box_size
            size = 7 * box_size
            
            draw.rounded_rectangle([x, y, x + size, y + size], radius=box_size * 2, fill=255)
            draw.rounded_rectangle([x + box_size, y + box_size, x + size - box_size, y + size - box_size], radius=box_size * 1.5, fill=0)
            draw.rounded_rectangle([x + box_size * 2, y + box_size * 2, x + size - box_size * 2, y + size - box_size * 2], radius=box_size, fill=255)

        draw_one(0, 0)
        draw_one(0, q_size - 7)
        draw_one(q_size - 7, 0)

    @staticmethod
    def _create_gradient(size) -> Image.Image:
        gradient_small = Image.new("RGB", (2, 2))
        gradient_small.putpixel((0, 0), (131, 58, 180))
        gradient_small.putpixel((1, 0), (253, 29, 29))
        gradient_small.putpixel((0, 1), (253, 29, 29))
        gradient_small.putpixel((1, 1), (252, 176, 69))
        return gradient_small.resize((size, size), resample=Image.Resampling.BILINEAR).convert("RGBA")

    @staticmethod
    def _embed_logo(img, img_size):
        draw = ImageDraw.Draw(img)
        center_box_size = img_size // 4
        center_x = (img_size - center_box_size) // 2
        center_y = (img_size - center_box_size) // 2
        
        draw.rounded_rectangle(
            [center_x, center_y, center_x + center_box_size, center_y + center_box_size],
            radius=20, fill="white", outline="white", width=5
        )
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__)) 
            services_dir = os.path.dirname(current_dir) 
            app_dir = os.path.dirname(services_dir) 
            
            logo_path = os.path.join(app_dir, "logo.png")
            
            if os.path.exists(logo_path):
                logo = Image.open(logo_path).convert("RGBA")
                logo_size = int(center_box_size * 0.8)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                logo_x = center_x + (center_box_size - logo_size) // 2
                logo_y = center_y + (center_box_size - logo_size) // 2
                img.paste(logo, (logo_x, logo_y), logo)
                
        except Exception as e:
            logger.error(f"Failed to embed logo: {e}")
