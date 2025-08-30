import os
from dotenv import load_dotenv
from utils.logger import setup_logger
from services.youtube import download_audio
from services.transcript import get_youtube_transcript, transcribe_with_whisper
from services.gemini import init_gemini, summarize, ask_question_stream
from rich.console import Console

console = Console()

def main():
    setup_logger()
    load_dotenv()
    init_gemini(os.getenv("GEMINI_API_KEY"))

    url = console.input("[bold green]Enter YouTube URL:[/bold green] ").strip()
    chat_history = []

    transcript, lang = get_youtube_transcript(url)

    if not transcript:
        console.print("[red]No captions found. Falling back to Whisper...[/red]")
        audio_file = download_audio(url)
        if audio_file:
            transcript = transcribe_with_whisper(audio_file)
            lang = "auto"

    if not transcript:
        console.print("[bold red]Transcript not available.[/bold red]")
        return

    console.print(f"\n[bold green]Chosen subtitle language:[/bold green] {lang}")
    console.print("\n=== [bold cyan]SUMMARY[/bold cyan] ===\n")
    summarize(transcript)

    while True:
        question = console.input("\n[bold green]Ask a question (or 'exit' to quit):[/bold green] ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        answer = ask_question_stream(transcript, question, chat_history)
        chat_history.append((question, answer))

if __name__ == "__main__":
    main()
