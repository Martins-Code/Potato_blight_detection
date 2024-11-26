from fastapi import FastAPI, UploadFile, File
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

MODEL = tf.keras.models.load_model("../models/model_1.keras")
CLASS_NAMES = ['Early_blight', 'Late_blight', 'Healthy']

@app.get('/ping')
async def ping():
    return {"message": "Hello, I'm alive!"}

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ['image/jpeg', 'image/png']:
        return {"error": "Invalid file type. Please upload a JPEG or PNG image."}

    try:
        # Read and preprocess the image
        image = read_file_as_image(await file.read())
        image_batch = np.expand_dims(image, 0)

        # Predict with the model
        predictions = MODEL.predict(image_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))  # Convert to Python float

        return {
            'class': predicted_class,
            'confidence': confidence
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=8080)
