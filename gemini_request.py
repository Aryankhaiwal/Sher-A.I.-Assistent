import google.generativeai as genai
import conf  

import google.generativeai as genai
import conf
import base64
from PIL import Image
from io import BytesIO

genai.configure(api_key=conf.geminiai_key)

text_model = genai.GenerativeModel("gemini-1.5-flash")

image_model = genai.GenerativeModel("gemini-1.5-flash")

def send_request(prompt: str):
    try:
        response = text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def generate_image(prompt: str, filename="generated.png"):
    try:
        response = image_model.generate_content(
            [prompt],
            generation_config={"response_mime_type": "image/png"}
        )
        
        
        image_data = response.candidates[0].content.parts[0].inline_data.data
        img = Image.open(BytesIO(base64.b64decode(image_data)))
        img.save(filename)
        return filename
    except Exception as e:
        return f"Error generating image: {e}"


