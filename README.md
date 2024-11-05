# Viseme Processing Service

A Python-based service for converting audio files into viseme timing sequences. This tool uses whisper.cpp for speech recognition and converts the output into viseme sequences suitable for facial animation.

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
The service will automatically download and compile whisper.cpp and required models on first run.

## Usage

### As a Command Line Tool

Process an audio file directly:

```bash
python viseme_processor.py input_audio.wav --output output.timing
```

Options:
- `--output`: Specify output file path (optional)
- `--install-path`: Custom installation path for whisper.cpp (optional)

### As a Web Service

Start the FastAPI server:

```bash
python vis_server.py
```

The server will start on `http://localhost:8000` by default.

#### API Endpoints

1. `POST /process/`
   - Upload a WAV file for processing
   - Returns JSON with viseme timing data

2. `GET /health/`
   - Health check endpoint
   - Returns server status

### API Examples

Using curl:
```bash
curl -X POST "http://localhost:8000/process/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_audio.wav"
```

## Output Format

The service generates JSON timing data with the following structure:

```json
[
    {
        "time": 0,
        "type": "viseme",
        "value": "sil"
    },
    {
        "time": 100,
        "type": "word",
        "value": "hello",
        "start": 100,
        "end": 500
    },
    {
        "time": 100,
        "type": "viseme",
        "value": "h"
    }
    // ... more visemes
]
```

## Viseme Types

The system uses the following viseme mappings:
https://docs.aws.amazon.com/polly/latest/dg/ph-table-english-uk.html

#
