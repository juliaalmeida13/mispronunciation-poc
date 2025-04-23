from fastapi import FastAPI, File, UploadFile, Form
import shutil
import os
import uuid
from utils.tools import extrair_audio_do_video, compactar_video
from transcricao import transcrever_audio
from llms.gemini_voz import analisar_audio_com_gemini
from llms.openai_voz import analisar_audio_com_gpt4

app = FastAPI()


@app.post("/validar_pronuncia/")
async def validar_pronuncia(
    arquivo: UploadFile = File(...),
    palavra_esperada: str = Form(...)
):
    # Salvar vídeo temporário
    nome_arquivo = f"uploads/video/{uuid.uuid4()}_{arquivo.filename}"
    with open(nome_arquivo, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    # Extrair e compactar vídeo
    video_compactado = compactar_video(nome_arquivo)
    caminho_audio = extrair_audio_do_video(video_compactado)
    caminho_pronuncia_correta = "uploads/audio/The Invisible Solar Expertise.mp3"

    # Transcrever com Whisper
    transcricao = transcrever_audio(caminho_audio)

    # Análise com Gemini Flash
    resposta_gemini = analisar_audio_com_gemini(caminho_audio,
                                                palavra_esperada,
                                                caminho_pronuncia_correta)
    resposta_openai = analisar_audio_com_gpt4(transcricao, palavra_esperada)

    # Limpeza
    os.remove(nome_arquivo)
    os.remove(video_compactado)
    os.remove(caminho_audio)

    return {
        "palavra_esperada": palavra_esperada,
        "transcricao": transcricao,
        "gemini_resposta": resposta_gemini,
        "openai_resposta": resposta_openai
    }
