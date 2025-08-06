from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp
import os
import uuid

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/download")
async def download(url: str):
    try:
        video_id = str(uuid.uuid4())
        output_path = f"{video_id}.mp4"

        ydl_opts = {
            "outtmpl": output_path,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

        return FileResponse(
            path=output_path,
            filename=info_dict.get("title", "video") + ".mp4",
            media_type="video/mp4"
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
