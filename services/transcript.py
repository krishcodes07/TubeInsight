"""
==================================================================
   Transcript Service Module
   -------------------------
   Provides utilities for:
   - Fetching YouTube transcripts via external service (youtubetotranscript.com/transcript)
   - Transcribing audio with Whisper model if external service failed
   - Saving transcripts with video metadata
==================================================================
"""

import logging
import requests
import whisper
from bs4 import BeautifulSoup
import os

# Cached Whisper model (loaded once and reused to save memory/time)
_whisper_model = None 


# --------------------------------------------------------------
# Function: get_whisper_model
# Purpose : Lazily load and return a Whisper model instance.
# Notes   : Uses the "small" model for efficiency.
# --------------------------------------------------------------
def get_whisper_model():
    """
    Load Whisper model only once and reuse it.
    
    Returns:
        whisper.Whisper: Loaded Whisper model instance.
    """
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("small")
    return _whisper_model


# --------------------------------------------------------------
# Function: save_transcript_with_metadata
# Purpose : Save transcript into a file with YouTube video metadata
#           written at the top for context.
# Notes   : Description is truncated to 150 chars if too long.
# --------------------------------------------------------------
def save_transcript_with_metadata(video_info: dict, transcript: str):
    """
    Save transcript to file with video metadata at the top.

    Args:
        video_info (dict): Dictionary containing title, channel, views, description.
        transcript (str): Transcript text to be saved.
    """
    try:
        # Ensure `data` directory exists
        os.makedirs("data", exist_ok=True)

        # Truncate description for readability
        description = video_info['description']
        if len(description) > 150:
            description = description[:150] + "..."

        # Save transcript and metadata into a text file
        with open("data/transcript.txt", "w", encoding="utf-8") as f:
            f.write(
                f"Title: {video_info['title']}\n"
                f"Channel: {video_info['channel']}\n"
                f"Views: {video_info['views']}\n"
                f"Description: {description}\n\n"
                f"Transcript:\n\n{transcript}"
            )
    except Exception as e:
        logging.error(f"Error saving transcript: {e}")


# --------------------------------------------------------------
# Function: get_youtube_transcript
# Purpose : Fetch transcript directly from youtubetotranscript.com
#           using the video URL.
# Returns : (transcript_text, source_type)
#           - source_type = "auto" if generated, None otherwise.
# --------------------------------------------------------------
def get_youtube_transcript(url: str) -> tuple[str, str | None]:
    """
    Fetch a transcript from YouTube using an external service.

    Args:
        url (str): YouTube video URL.

    Returns:
        tuple: (transcript text, source type) 
               where source type is "auto" or None.
    """
    transcript_url = "https://youtubetotranscript.com/transcript"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://youtubetotranscript.com",
        "Referer": "https://youtubetotranscript.com/"
    }

    # Try to fetch transcript HTML
    try:
        response = requests.post(transcript_url, headers=headers, data={"youtube_url": url}, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Transcript fetch request failed: {e}")
        return "", None

    # Import lazily to avoid circular dependency
    from services.youtube import get_video_info
    video_info = get_video_info(url)

    # Parse HTML response for transcript segments
    soup = BeautifulSoup(response.content, "html.parser")
    segments = soup.find_all("span", class_="transcript-segment")

    if not segments:
        logging.warning("No transcript found.")
        return "", None

    # Join text from all transcript segments
    transcript = " ".join(seg.get_text(strip=True) for seg in segments if seg.get_text(strip=True))

    if transcript:
        save_transcript_with_metadata(video_info, transcript)
        return transcript, "auto"

    return "", None


# --------------------------------------------------------------
# Function: transcribe_with_whisper
# Purpose : Transcribe a downloaded audio file using Whisper model.
# Notes   : Also saves transcript with video metadata.
# --------------------------------------------------------------
def transcribe_with_whisper(audio_file: str, url: str) -> str:
    """
    Transcribe audio file with Whisper and save with metadata.

    Args:
        audio_file (str): Path to the audio file.
        url (str): YouTube video URL for fetching metadata.

    Returns:
        str: Transcribed text.
    """
    try:
        # Load Whisper model (cached after first call)
        model = get_whisper_model()
        result = model.transcribe(audio_file, language="en")
        text = result.get("text", "").strip()

        # Import lazily to avoid circular dependency
        from services.youtube import get_video_info
        video_info = get_video_info(url)

        # Save transcript if text exists
        if text:
            save_transcript_with_metadata(video_info, text)

        return text
    except Exception as e:
        logging.error(f"Whisper transcription error: {e}")
        return ""
