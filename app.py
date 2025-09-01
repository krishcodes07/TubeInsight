"""
==================================================================

███╗░░░███╗░█████╗░██████╗░███████╗  ██████╗░██╗░░░██╗  ██╗░░██╗██████╗░██╗░██████╗██╗░░██╗
████╗░████║██╔══██╗██╔══██╗██╔════╝  ██╔══██╗╚██╗░██╔╝  ██║░██╔╝██╔══██╗██║██╔════╝██║░░██║
██╔████╔██║███████║██║░░██║█████╗░░  ██████╦╝░╚████╔╝░  █████═╝░██████╔╝██║╚█████╗░███████║
██║╚██╔╝██║██╔══██║██║░░██║██╔══╝░░  ██╔══██╗░░╚██╔╝░░  ██╔═██╗░██╔══██╗██║░╚═══██╗██╔══██║
██║░╚═╝░██║██║░░██║██████╔╝███████╗  ██████╦╝░░░██║░░░  ██║░╚██╗██║░░██║██║██████╔╝██║░░██║
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═════╝░╚══════╝  ╚═════╝░░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝

==================================================================
                   Made with ❤️ by Krish
==================================================================
"""

import os
from dotenv import load_dotenv
from utils.logger import setup_logger
from services.youtube import download_audio, get_video_info
from services.transcript import get_youtube_transcript, transcribe_with_whisper
from services.gemini import init_gemini, summarize, ask_question_stream
from rich.console import Console

console = Console()


# --------------------------------------------------------------
# Function: main
# Purpose : Entry point of the application.
# Notes   : 
#   1. Loads environment variables and API keys
#   2. Fetches transcript (from "youtubetotranscript.com/transcript" or Whisper if error)
#   3. Displays video metadata
#   4. Summarizes video using Gemini
#   5. Provides interactive Q&A with chat history
# --------------------------------------------------------------
def main():
    setup_logger()
    load_dotenv()
    init_gemini(os.getenv("GEMINI_API_KEY"))

    # Step 1: Ask user for YouTube URL
    url = console.input("[bold green]Enter YouTube URL:[/bold green] ").strip()
    chat_history = []

    # Step 2: Try fetching transcript from youtubetotranscript.com/transcript
    transcript, lang = get_youtube_transcript(url)

    # Step 3: If no transcript found, fall back to Whisper
    if not transcript:
        console.print("[red]No captions found. Falling back to Whisper...[/red]")
        audio_file = download_audio(url)
        if audio_file:
            transcript = transcribe_with_whisper(audio_file, url)
            lang = "auto"

    if not transcript:
        console.print("[bold red]Transcript not available.[/bold red]")
        return

    # Step 4: Show video metadata
    video_info = get_video_info(url)
    console.print("\n=== [bold cyan]VIDEO INFO[/bold cyan] ===")
    console.print(f"[bold green]Title:[/bold green] {video_info['title']}")
    console.print(f"[bold cyan]Channel:[/bold cyan] {video_info['channel']}")
    console.print(f"[bold yellow]Views:[/bold yellow] {video_info['views']}")
    console.print(f"[bold white]Description:[/bold white] {video_info['description'][:300]}...\n")

    console.print(f"\n[bold green]Chosen subtitle language:[/bold green] {lang}")

    # Step 5: Generate summary
    console.print("\n=== [bold cyan]SUMMARY[/bold cyan] ===\n")
    summarize(transcript, video_info)

    # Step 6: Interactive Q&A loop
    while True:
        question = console.input("\n[bold green]Ask a question (or 'exit' to quit):[/bold green] ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        answer = ask_question_stream(transcript, video_info, question, chat_history)
        chat_history.append((question, answer))


if __name__ == "__main__":
    main()
