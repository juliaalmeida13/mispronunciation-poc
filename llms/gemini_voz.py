import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re
from rich import print

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL")

genai.configure(api_key=GEMINI_API_KEY)


def analisar_audio_com_gemini(caminho_audio, palavra):
    model = genai.GenerativeModel(MODEL)

    with open(caminho_audio, "rb") as f:
        audio_bytes = f.read()

    prompt = f"""
        Você é um especialista em fonética do português brasileiro. 
        Seu papel é avaliar se um criador de conteúdo pronunciou corretamente a palavra "{palavra}" no áudio a seguir.

        Responda APENAS no formato JSON, com as seguintes chaves:
        - "avaliacao": uma das opções ["correta", "aceitável", "incorreta"]
        - "justificativa": texto explicando por que foi considerada correta, aceitável ou incorreta, incluindo observações sobre sotaque, clareza, etc.
        - "correcao_sugerida": se for "incorreta", indique como a pronúncia deveria soar

        Exemplo de resposta:

        {{
            "avaliacao": "aceitável",
            "justificativa": "A palavra foi pronunciada com sotaque nordestino leve, mas ainda inteligível.",
            "correcao_sugerida": null
        }}

        Se estiver correta, use "correcao_sugerida": null
        Se estiver incorreta, traga a pronúncia ideal fonética (ex: /ˈkɔkɐ ˈkɔlɐ/)
"""
    print("[bold blue]Analisando áudio com Gemini Flash...[/bold blue]")
    response = model.generate_content(
        [
            prompt,
            {
                "mime_type": "audio/mp3",  # ou "audio/mp3"
                "data": audio_bytes
            }
        ],
        stream=False
    )

    try:
        # Extrai JSON dentro de blocos ```json ... ``` se houver
        raw = response.text.strip()
        if "```json" in raw:
            raw = re.search(r"```json\n(.*)\n```", raw, re.DOTALL).group(1)

        dados = json.loads(raw)
    except Exception:
        dados = {
            "avaliacao": "erro",
            "justificativa": "Não foi possível interpretar a resposta do modelo.",
            "correcao_sugerida": None,
            "resposta_original": response.text
        }

    return dados
