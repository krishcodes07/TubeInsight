import logging
import google.generativeai as genai
from rich.console import Console

console = Console()


def init_gemini(api_key: str):
    """
    Configure Gemini with API key.
    """
    genai.configure(api_key=api_key)


def summarize(transcript: str) -> str:
    """
    Summarize transcript with Gemini (streaming, yellow output).
    """
    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction="You are given a YouTube transcript. Summarize briefly."
        )

        console.print("[bold green]Summary:[/bold green]\n")

        response_stream = model.generate_content(
            f"YouTube transcript:\n\n{transcript}",
            stream=True
        )

        final_text = ""
        for chunk in response_stream:
            if chunk.text:
                console.print(chunk.text, end="", style="yellow")
                final_text += chunk.text

        console.print()
        return final_text

    except Exception as e:
        logging.error(f"Gemini streaming summarization error: {e}")
        return ""


def ask_question_stream(transcript: str, question: str, chat_history: list | None = None) -> str:
    """
    Ask a question about transcript with Gemini (streaming, green output).
    """
    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction="Answer concisely using transcript + chat history."
        )

        prompt = f"Transcript: {transcript}\n\n"
        if chat_history:
            for i, (q, a) in enumerate(chat_history[-10:], 1):
                prompt += f"Q{i}: {q}\nA{i}: {a}\n\n"
        prompt += f"Current Question: {question}"

        console.print("[bold cyan]Answer:[/bold cyan]\n")

        response_stream = model.generate_content(prompt, stream=True)
        final_text = ""

        for chunk in response_stream:
            if chunk.text:
                console.print(chunk.text, end="", style="yellow")
                final_text += chunk.text

        console.print()
        return final_text

    except Exception as e:
        logging.error(f"Gemini streaming Q&A error: {e}")
        return ""
