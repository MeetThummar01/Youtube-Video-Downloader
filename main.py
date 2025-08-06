from fastapi import FastAPI
app = FastAPI()
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from yt_dlp import YoutubeDL
import os

app = FastAPI()

# Mount the static directory to serve index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/download")
async def download(url: str):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return JSONResponse({
                "title": info_dict.get("title"),
                "formats": info_dict.get("formats", []),
                "thumbnail": info_dict.get("thumbnail"),
                "uploader": info_dict.get("uploader"),
            })
    except Exception as e:
        return JSONResponse({"error": str(e)})

