import uuid
from fastapi import FastAPI, File, UploadFile
from predictory import DeptEstimationModel
import os


app = FastAPI()
depth_estimation = DeptEstimationModel()
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"]
TEMP_FOLDER = "api_images"
os.makedirs(TEMP_FOLDER, exist_ok=True)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1]
        if file_ext.lower() not in ALLOWED_EXTENSIONS:
            return {
                "error": "Unsupported file type. Please upload a JPG, JPEG or PNG image."
            }
        filename_base = str(uuid.uuid4())
        filename = filename_base + file_ext
        destination_path = os.path.join(TEMP_FOLDER, filename)
        output_path = os.path.join(TEMP_FOLDER, "output" + filename_base + ".png")

        with open(destination_path, "wb") as image_data:
            image_data.write(file.file.read())

        depth_estimation.calculate_depthmap(destination_path, output_path)
        return {"OK": "Image processed successfully"}
    except Exception as e:
        return {"error": str(e)}
