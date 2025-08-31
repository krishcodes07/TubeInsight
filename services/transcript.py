import logging
import requests
import whisper
from bs4 import BeautifulSoup

_whisper_model = None 

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("small")
    return _whisper_model

def get_youtube_transcript(url: str) -> tuple[str, str | None]:
    transcript_url = "https://youtubetotranscript.com/transcript"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://youtubetotranscript.com",
        "Referer": "https://youtubetotranscript.com/"
    }

    try:
        response = requests.post(transcript_url, headers=headers, data={"youtube_url": url}, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Transcript fetch request failed: {e}")
        return "", None

    soup = BeautifulSoup(response.content, "html.parser")
    segments = soup.find_all("span", class_="transcript-segment")

    if not segments:
        logging.warning("No transcript found.")
        return "", None

    transcript = " ".join(seg.get_text(strip=True) for seg in segments if seg.get_text(strip=True))
    if transcript:
        with open("data/transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
        return transcript, "auto"
    return "", None

def transcribe_with_whisper(audio_file: str) -> str:
    try:
        model = get_whisper_model()
        result = model.transcribe(audio_file, language="en")
        text = result.get("text", "").strip()
        if text:
            with open("data/transcript.txt", "w", encoding="utf-8") as f:
                f.write(text)
        return text
    except Exception as e:
        logging.error(f"Whisper transcription error: {e}")
        return ""
