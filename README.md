# TubeInsight

**TubeInsight** is a Python-based tool that extracts YouTube video transcripts, summarizes them using gemini-1.5-pro, and allows interactive Q\&A about the content. It also integrates OpenAI Whisper for audio transcription if captions are unavailable.

---

## Features

* Fetch YouTube video transcripts automatically. reveresed engined - https://youtubetotranscript.com/transcript
* Fallback to **Whisper** for audio transcription if subtitles are missing.
* Summarize transcripts concisely using **gemini-2.5-flash**.
* Ask questions interactively about the video content, with AI-powered streaming responses.
* Colorful, user-friendly terminal interface using **Rich**.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/krishcodes07/TubeInsight.git
cd TubeInsight
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

Run the main application:

```bash
python app.py
```

1. Enter the YouTube URL when prompted.
2. The transcript will be fetched. If unavailable, audio will be downloaded and transcribed using Whisper.
3. A summary of the video will be displayed.
4. Ask questions about the video interactively in the terminal.
5. Type `exit` or `quit` to stop.

---

## Project Structure

```
TubeInsight/
│
├─ app.py                # Main script
├─ .env                  # Environment variables (API keys)
├─ requirements.txt      # Python dependencies
├─ data/                 # Transcripts saved here
├─ utils/
│  └─ logger.py          # Rich logging setup
├─ services/
│  ├─ youtube.py         # YouTube audio downloader
│  ├─ transcript.py      # Transcript fetching & Whisper transcription
│  └─ gemini.py          # Gemini AI summarization & Q&A
└─ README.md
```

---

## Dependencies

* [Rich](https://pypi.org/project/rich/) – For colorful terminal output
* [Whisper](https://github.com/openai/whisper) – Audio transcription
* [pytubefix](https://pypi.org/project/pytubefix/) – YouTube video download
* [Requests](https://pypi.org/project/requests/) – HTTP requests
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) – HTML parsing
* [Google Generative AI](https://pypi.org/project/google-generative-ai/) – Gemini AI interaction

---

## Notes

* Make sure you have a stable internet connection for transcript fetching and Gemini API calls.
* Audio transcription may take longer depending on video length.
* Transcript files are saved in the `data/` folder for reuse.


---

## License

MIT License © 2025
Developed by **Krish**
