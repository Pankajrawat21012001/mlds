# backend.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import openai
import os
from io import StringIO

app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key (consider using environment variables for security)
openai.api_key = os.getenv("OPENAI_API_KEY", "your_default_api_key_here")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()

        # Extract the actual file name
        file.filename = file.filename.split('|')[0]

        # Check the file extension
        if file.filename.endswith('.csv'):
            df = pd.read_csv(StringIO(contents.decode('utf-8')))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(contents)  # Read directly from the file-like object
        else:
            return JSONResponse(content={"error": "Unsupported file type. Please upload a CSV or Excel file."}, status_code=400)

        # Check if the DataFrame is empty
        if df.empty:
            return JSONResponse(content={"error": "The uploaded file is empty."}, status_code=400)

        # Perform analysis (this is a placeholder for your analysis logic)
        analysis_result = analyze_data(df)
        
        return JSONResponse(content={"result": analysis_result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def analyze_data(df):
    # Example analysis: Calculate total sales
    total_sales = df['Sales'].sum()
    return {"total_sales": total_sales}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)