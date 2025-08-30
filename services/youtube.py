import os
import logging
from pytubefix import YouTube as PTFixYouTube

def get_video_id(url: str) -> str | None:
    import re
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def download_audio(url: str, filename: str = "audio.mp3") -> str:
    try:
        yt = PTFixYouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            raise ValueError("No audio streams available")

        out_file = stream.download(filename="temp_audio.mp4")
        os.replace(out_file, filename)
        return filename
    except Exception as e:
        logging.error(f"Audio download error: {e}")
        return ""
