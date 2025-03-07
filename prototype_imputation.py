from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

IMPUTED_FILE_PATH = "/Users/nivedharengaraj/Downloads/Major project/Imputateddata.csv"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:3002"] if that's where your HTML is served
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
   
    try:
        
        df = pd.read_csv(file.file)
        df["Imputed"] = "dummy_value"

        # 3. Save as 'imputed_dataset.csv'
        df.to_csv(IMPUTED_FILE_PATH, index=False)

        return {"message": "File uploaded and imputed CSV created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/download/")
def download_imputed(model: str = "SAITS"):
    if model == "SAITS":
        file_path = "/absolute/path/to/saits_imputed_dataset.csv"
        download_filename = "saits_imputed_dataset.csv"
    elif model == "BRITS":
        file_path = "/absolute/path/to/brits_imputed_dataset.csv"
        download_filename = "brits_imputed_dataset.csv"
    elif model == "LOCF":
        file_path = "/absolute/path/to/locf_imputed_dataset.csv"
        download_filename = "locf_imputed_dataset.csv"
    else:
        raise HTTPException(status_code=400, detail="Unknown model name.")

    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            filename=download_filename,
            media_type="text/csv"
        )
    else:
        raise HTTPException(status_code=404, detail=f"No file found for {model}. Upload first.")

