import requests
# from PIL import Image
import os


class ImageInfoWrapper:

    def __init__(self):

        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY')}"
        }

        self.api_url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"


    def get_image_info(self, img):

        # raw_image = Image.open(img).convert("RGB")
        # text = "This image is uploaded to search the internet. What are some relevant keywords that can be extracted from this image?"

        response = requests.post(
            self.api_url,
            headers = self.headers,
            data = img
        )

        return response.json()

