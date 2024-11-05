from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import tempfile
import uvicorn
from typing import Optional
import shutil
import json
from viseme_processor import VisemeProcessor, process_audio_file  # assuming the original code is in viseme_processor.py

app = FastAPI(
    title="Viseme Processing API",
    description="API for converting audio files to viseme timing files",
    version="1.0.0"
)

# Initialize the VisemeProcessor
processor = VisemeProcessor()

@app.on_event("startup")
async def startup_event():
    """Ensure whisper is installed on startup"""
    try:
        processor.ensure_installed()
    except Exception as e:
        print(f"Error during startup: {e}")
        raise

@app.post("/process/", response_class=JSONResponse)
async def process_audio(file: UploadFile = File(...)):
    """
    Process an audio file and return viseme timings
    
    Args:
        file: Uploaded audio file (WAV format)
        
    Returns:
        JSON response with viseme timings
    """
    if not file.filename.lower().endswith('.wav'):
        raise HTTPException(status_code=400, detail="Only WAV files are supported")
    
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Save uploaded file
            temp_audio = temp_dir_path / "input.wav"
            with temp_audio.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process the audio file
            temp_output = temp_dir_path / "output.timing"
            processor.process_audio(temp_audio, temp_output)
            
            # Read the timing file
            with open(temp_output, 'r') as f:
                timing_data = [json.loads(line) for line in f]
            
            return JSONResponse(content=timing_data)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()

@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
