import os
from openai import OpenAI
import json
import re
from dotenv import load_dotenv
from rich import print

# Carregar variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Carregar Whisper localmente
def analisar_audio_com_gpt4(transcricao, palavra):

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Prompt fonético para GPT-4
    prompt = f"""
        Você é um especialista em fonética do português brasileiro e atua como avaliador de pronúncia em vídeos publicitários.

        Seu objetivo é avaliar se o nome da Palavra abaixo foi pronunciado corretamente no áudio enviado.

        Palavra a ser validada: "{palavra}"
        transcrição: "{transcricao}"

        Avalie com base nos critérios:
        1. A Palavra foi pronunciada?
        2. A fonética foi correta ou aceitável?
        3. A pronúncia foi clara, fluida e natural?
        4. O ritmo e a entonação foram adequados?

        Considere sotaques brasileiros e pronúncias adaptadas ao português como aceitáveis, desde que mantenham clareza.

        Responda **somente no formato JSON**:

        {{
        "avaliacao": "correta" | "aceitável" | "incorreta",
        "justificativa": "explicação fonética detalhada",
        "correcao_sugerida": null | "pronúncia ideal (AFI ou adaptada)",
        "nivel_confianca": número entre 0.0 e 1.0
        }}
    """

    print("[bold blue]Analisando com GPT-4...[/bold blue]")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um linguista especialista em fonética brasileira."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    try:
        raw = response.choices[0].message.content.strip()
        if "```json" in raw:
            raw = re.search(r"```json\\n(.*)\\n```", raw, re.DOTALL).group(1)

        dados = json.loads(raw)
    except Exception:
        dados = {
            "avaliacao": "erro",
            "justificativa": "Não foi possível interpretar a resposta do modelo.",
            "correcao_sugerida": None,
            "nivel_confianca": None,
            "resposta_original": response.choices[0].message.content
        }

    return dados
