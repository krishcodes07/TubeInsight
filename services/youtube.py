import os
import logging
from pytubefix import YouTube as PTFixYouTube
import re

def get_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from different URL formats.
    Works for:
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtube.com/embed/VIDEO_ID
    - https://youtube.com/shorts/VIDEO_ID
    - With extra params like ?si=...
    """
    pattern = (
        r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))"
        r"([0-9A-Za-z_-]{11})"
    )
    match = re.search(pattern, url)
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
