from fastapi import FastAPI, UploadFile, File
import shutil
import os

from backend.app.ingestion.raster import inspect_raster


app = FastAPI(title="SatQuery AI")


@app.get("/")
def root():
    return {
        "message": "SatQuery AI API is running"
    }


@app.post("/inspect-raster")
def inspect_uploaded_raster(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    metadata = inspect_raster(file_path)

    return {
        "filename": file.filename,
        "metadata": metadata
    }