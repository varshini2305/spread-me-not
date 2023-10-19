# python credibility_checker/fetch_image.py
import requests
from pathlib import Path
from PIL import Image
import pytesseract
import logging

def download_image(url, save_path=None, filename: str = None):
    response = requests.get(url)
    
    if response.status_code == 200:
        if save_path is None:
            # Extract the filename from the URL
            if filename is None:
                filename = url.split("/")[-1]
            save_path = Path(filename)
        
        with open(save_path, 'wb') as file:
            file.write(response.content)
            
        print(f"Image downloaded and saved as {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
    return filename

# Path to the Tesseract executable (update the path based on your installation)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)

    return text

def extract_text_from_url(image_url: str = None, image_path: str = None):
    try:
        download_image(image_url, filename=image_path)
        extracted_text = extract_text_from_image(image_path)
    except Exception:
        logging.exception("traceback as follows: ")
        extracted_text = ''
    return extracted_text


# Example usage
image_path = 'tweet_images/tweet.jpeg'
image_url = "https://pbs.twimg.com/media/F8kQUcPXwAEjFdx.jpg"
image_path = download_image(image_url)

extracted_text = extract_text_from_image(image_path)
print(f"Extracted Text: {extracted_text}")