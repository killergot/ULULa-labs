from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from typing import List
import uvicorn

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/subjects/multiple_files")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(file.filename)
    return {"uploaded_files": saved_files}


@app.get("/subjects/upload/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')

if __name__ == "__main__":
    uvicorn.run(app, port=8000,workers=2)