import os
import requests
from time import sleep

def save_image_locally(img_url):
    if img_url.startswith("data:image"):
        return "N/A"  # Skip saving or handle accordingly

    try:
        img_data = requests.get(img_url).content
        img_name = img_url.split("/")[-1]
        with open(f"images/{img_name}", 'wb') as handler:
            handler.write(img_data)
        return f"images/{img_name}"
    except Exception as e:
        print(f"Failed to save image: {e}")
        return "N/A"

def retry(func):
    def wrapper(*args, **kwargs):
        retries = 3
        while retries > 0:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException:
                retries -= 1
                sleep(5)
                if retries == 0:
                    raise
    return wrapper
