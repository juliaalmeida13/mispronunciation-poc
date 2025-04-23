import whisper
from rich import print

modelo = whisper.load_model("medium")


def transcrever_audio(caminho_audio):
    resultado = modelo.transcribe(caminho_audio, language='pt')
    print('[bold blue]Transcrição do áudio:[/bold blue]')
    print(resultado["text"])
    return resultado["text"].strip().lower()
