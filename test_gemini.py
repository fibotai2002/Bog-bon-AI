import asyncio
import os
from bot.services.gemini import analyze_image_with_gemini

# Mock image data (read a small file or create dummy bytes)
# We need a real image for Gemini to work well, but let's try with a small dummy first or fail.
# Better to use a real image if possible. Let's list files to find one.

async def main():
    print("Testing Gemini API...")
    try:
        # Create a dummy image or read one if exists
        with open("logo.png", "rb") as f:
            image_data = f.read()
            
        result = await analyze_image_with_gemini(image_data, "Test Plant")
        print("Result:", result)
    except Exception as e:
        print(f"Test Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
