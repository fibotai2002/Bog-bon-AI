"""
Rasm qayta ishlash utilities
"""

import io
import logging
from typing import Optional, Tuple
from PIL import Image

from bot.config import MAX_IMAGE_SIZE, JPEG_QUALITY

logger = logging.getLogger(__name__)

async def process_image(image_bytes: bytes) -> Optional[Tuple[bytes, dict]]:
    """
    Rasmni qayta ishlash: resize, compress, validate
    
    Args:
        image_bytes: Asl rasm bytes formatda
        
    Returns:
        Tuple[qayta ishlangan bytes, metadata dict] yoki None (xato bo'lsa)
        metadata: {"width": int, "height": int, "format": str, "size_kb": float}
    """
    try:
        # Rasmni ochish
        image = Image.open(io.BytesIO(image_bytes))
        original_format = image.format
        original_size = len(image_bytes)
        
        logger.info(f"Asl rasm: {image.size}, format: {original_format}, hajm: {original_size / 1024:.1f}KB")
        
        # RGB'ga o'tkazish (JPEG uchun kerak)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Alpha channel bo'lsa, oq fonga qo'yish
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize (agar kerak bo'lsa)
        width, height = image.size
        if width > MAX_IMAGE_SIZE or height > MAX_IMAGE_SIZE:
            # Aspect ratio saqlab resize
            if width > height:
                new_width = MAX_IMAGE_SIZE
                new_height = int(height * (MAX_IMAGE_SIZE / width))
            else:
                new_height = MAX_IMAGE_SIZE
                new_width = int(width * (MAX_IMAGE_SIZE / height))
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Rasm resize qilindi: {image.size}")
        
        # JPEG ga compress
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=JPEG_QUALITY, optimize=True)
        processed_bytes = output.getvalue()
        
        # Metadata
        metadata = {
            "width": image.size[0],
            "height": image.size[1],
            "format": "JPEG",
            "size_kb": len(processed_bytes) / 1024,
            "original_size_kb": original_size / 1024,
            "compression_ratio": original_size / len(processed_bytes)
        }
        
        logger.info(f"Qayta ishlangan: {metadata['width']}x{metadata['height']}, "
                   f"hajm: {metadata['size_kb']:.1f}KB, "
                   f"siqish: {metadata['compression_ratio']:.1f}x")
        
        return processed_bytes, metadata
        
    except Exception as e:
        logger.error(f"Rasm qayta ishlash xatosi: {e}", exc_info=True)
        return None

def validate_image_quality(metadata: dict) -> Tuple[bool, list]:
    """
    Rasm sifatini tekshirish
    
    Args:
        metadata: Rasm metadata
        
    Returns:
        Tuple[ok: bool, issues: list]
    """
    issues = []
    
    # Minimal o'lcham tekshiruvi (faqat juda kichik < 50px bo'lsa)
    min_size = 50
    if metadata["width"] < min_size or metadata["height"] < min_size:
        issues.append("too_small")
    
    # User talabi bo'yicha qattiq cheklovlar olib tashlandi
    # har doim True qaytariladi (agar juda kichik bo'lmasa)
    
    ok = len(issues) == 0
    
    # Agar baribir tahlil qilish kerak bo'lsa, har doim True qaytaramiz
    return True, issues

async def download_telegram_photo(bot, file_id: str) -> Optional[bytes]:
    """
    Telegram'dan rasmni yuklab olish
    
    Args:
        bot: Bot instance
        file_id: Telegram file ID
        
    Returns:
        Rasm bytes yoki None
    """
    try:
        # File ma'lumotlarini olish
        file = await bot.get_file(file_id)
        
        # Rasmni yuklab olish
        file_bytes = await bot.download_file(file.file_path)
        
        # BytesIO'dan bytes'ga o'tkazish
        if hasattr(file_bytes, 'read'):
            return file_bytes.read()
        return file_bytes
        
    except Exception as e:
        logger.error(f"Telegram rasm yuklab olish xatosi: {e}")
        return None
