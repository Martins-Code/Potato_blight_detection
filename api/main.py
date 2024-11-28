from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

# Allow CORS for React frontend
# Browsers block cross-origin requests (from a React app to a FastAPI server) by default for security reasons. Adding CORSMiddleware ensures that the frontend can communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update if  React app runs on a different port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and define class names
MODEL = tf.keras.models.load_model("../models/model_1.keras")
CLASS_NAMES = ['Early_blight', 'Late_blight', 'Healthy']

@app.get('/ping')
async def ping():
    return {"message": "Hello, I'm alive!"}

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")  # Ensure 3 color channels
    image = image.resize((224, 224))  # Resize to match model input size
    return np.array(image)

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ['image/jpeg', 'image/png']:
        return {"error": "Invalid file type. Please upload a JPEG or PNG image."}

    try:
        # Read and preprocess the image
        image = read_file_as_image(await file.read())
        image_batch = np.expand_dims(image, 0)  # Add batch dimension

        # Make predictions
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
