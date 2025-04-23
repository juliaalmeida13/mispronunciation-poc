import subprocess
import uuid


def extrair_audio_do_video(caminho_video):
    nome = str(uuid.uuid4())
    caminho_audio = f"uploads/audio/{nome}.mp3"

    comando = [
        "ffmpeg", "-i", caminho_video,
        "-q:a", "0", "-map", "a", caminho_audio, "-y"
    ]

    subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return caminho_audio


def compactar_video(caminho_video, resolucao="640x360"):
    nome_compactado = caminho_video.replace(".mp4", "_compactado.mp4")

    comando = [
        "ffmpeg", "-i", caminho_video,
        "-vf", f"scale={resolucao}",
        "-b:v", "500k",
        "-b:a", "96k",
        "-y", nome_compactado
    ]

    subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return nome_compactado
