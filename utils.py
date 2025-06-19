import os
import zipfile
import aiohttp
import random
from PIL import Image
from config import GIPHY_API_KEY


async def process_cover_image(original_path: str, resized_path: str):
    with Image.open(original_path) as img:
        img = img.convert("RGB")
        img.thumbnail((500, 500))
        img.save(resized_path, format="JPEG", quality=85)


def zip_file(input_path, output_path):
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(input_path, arcname=os.path.basename(input_path))


async def get_random_horse_gif():
    if not GIPHY_API_KEY:
        return "🐴"

    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.giphy.com/v1/gifs/search"
            params = {
                'api_key': GIPHY_API_KEY,
                'q': 'horse',
                'limit': 50,
                'rating': 'g',
                'lang': 'en'
            }

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['data']:
                        random_gif = random.choice(data['data'])
                        return random_gif['images']['original']['url']
    except Exception as e:
        print(f"Error fetching horse GIF: {e}")

    return "🐴"