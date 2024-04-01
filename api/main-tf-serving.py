import tensorflow as tf
import numpy as np
from fastapi import FastAPI, File , UploadFile
import uvicorn
from io import BytesIO
from PIL import Image
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=[
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
# MODEL=tf.keras.models.load_model(r"C:\Users\KIIT\OneDrive\Desktop\my-documents\programming\potato-disease\saved_models\1")

endpoint="http://localhost:8501/v1/models/potatoes_model:predict"

CLASS_NAMES= ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "hello, this is working"

def read_file_as_image(data)->np.ndarray:
    image=np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile=File(...)
): 
    image= read_file_as_image(await file.read())
    img_batch=np.expand_dims(image,0)
    
    json_data={
        "instances":img_batch.tolist()
    }

    response=requests.post(endpoint,json=json_data)
    # return response.json()

    prediction=np.array(response.json()["predictions"][0])
    
    predicted_class=CLASS_NAMES[np.argmax(prediction)]
    confidence=np.max(prediction)

    return {
        "class": predicted_class,
        "confidence": confidence
    }
    pass
    
    # predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    # confidence=np.max(prediction[0])*100
    
    # return{
    #     'class' : predicted_class,
    #     'confidence' : float(confidence)
    # }

if __name__ =="__main__" :
    uvicorn.run(app,host='localhost', port=8000)