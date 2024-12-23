from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.responses import JSONResponse
import torchaudio
import torch
from io import BytesIO
import gc

bundle = torchaudio.pipelines.WAV2VEC2_ASR_LARGE_960H
model = bundle.get_model()
app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/asr")
async def asr(file: UploadFile):
    try:
        file_bytes = await file.read()
        with BytesIO(file_bytes) as audio_file:
            audio, sample_rate = torchaudio.load(audio_file, format="mp3")
        duration = round(len(audio[0]) / sample_rate, 1)
        audio = torchaudio.functional.resample(audio, sample_rate, bundle.sample_rate)
        with torch.no_grad():
            emissions, _ = model(audio)
        indices = torch.argmax(emissions, dim=-1)
        indices = torch.unique_consecutive(indices, dim=-1)
        labels = bundle.get_labels()
        transcription = "".join([labels[i] for i in indices[0] if i > 0]).replace("|", " ")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        del file_bytes, audio, emissions, indices
        gc.collect()
        await file.close()

    return {"transcription": transcription, "duration": duration}