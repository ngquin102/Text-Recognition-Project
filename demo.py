import requests
import json
import gradio as gr
from PIL import Image
import numpy as np
import easyocr
import io

reader = easyocr.Reader(['en'])
def recognize_text(image=None, image_url=None):
    if image is not None:
        image_np = np.array(image)
        ocr_result = reader.readtext(image_np)
        transcription = ' '.join([res[1] for res in ocr_result])
        return transcription

    elif image_url:
        payload = json.dumps({"image_url": image_url})
        headers = {'Content-Type': 'application/json'}
        response = requests.post("http://10.100.200.119:1412/predict", headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            return json.dumps(data, indent=2)
        else:
            return f"Error: Unable to process the image. Status code: {response.status_code}"
    else:
        return "Please provide an image or URL."

# Tạo giao diện Gradio
interface = gr.Interface(
    fn=recognize_text,
    inputs=[gr.Image(type="pil"), gr.Textbox(lines=1, placeholder="Enter image URL ")],
    outputs=gr.Textbox(),
    title="Text Recognition Demo",
    description="Upload an image or enter an image URL"
)

if __name__ == "__main__":
    interface.launch()
