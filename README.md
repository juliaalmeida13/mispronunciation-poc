# Detect Correct Pronunciation

Este projeto é uma API desenvolvida com FastAPI para validar a pronúncia de palavras em vídeos enviados. Ele utiliza modelos de IA, como Whisper, Gemini Flash e GPT-4, para transcrever e avaliar a pronúncia de palavras em português brasileiro.

## Estrutura do Projeto

```
.env
.envexample
.gitignore
main.py
requirements.txt
llms/
    llms/gemini_voz.py
    llms/openai_voz.py
uploads/
    audio/
    video/
utils/
    utils/tools.py
    utils/transcricao.py
```

### Principais Arquivos e Diretórios

- **`main.py`**: Arquivo principal que define a API e seus endpoints.
- **`llms/`**: Contém os módulos para integração com os modelos de IA (Gemini Flash e GPT-4).
- **`utils/`**: Contém utilitários para manipulação de vídeos e transcrição de áudio.
- **`uploads/`**: Diretório para armazenar arquivos de áudio e vídeo enviados.

## Funcionalidades

1. **Upload de Vídeo**: O usuário pode enviar um vídeo para validação.
2. **Extração de Áudio**: O áudio é extraído do vídeo utilizando `ffmpeg`.
3. **Transcrição**: O áudio é transcrito usando o modelo Whisper.
4. **Validação de Pronúncia**:
   - **Gemini Flash**: Avalia a pronúncia com base em um prompt fonético.
   - **GPT-4**: Realiza uma análise detalhada da pronúncia com base na transcrição.
5. **Resposta JSON**: A API retorna uma resposta JSON com as avaliações dos modelos.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/detect-correct-pronunciation.git
   cd detect-correct-pronunciation
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Renomeie o arquivo `.envexample` para `.env`.
   - Preencha as chaves de API (`GEMINI_API_KEY`, `OPENAI_API_KEY`, etc.) no arquivo `.env`.

5. Certifique-se de ter o `ffmpeg` instalado no sistema.

## Uso

1. Inicie o servidor FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

2. Acesse a documentação interativa da API em:
   ```
   http://127.0.0.1:8000/docs
   ```

3. Utilize o endpoint `/validar_pronuncia/` para enviar um vídeo e validar a pronúncia de uma palavra.

## Exemplo de Resposta da API

```json
{
  "palavra_esperada": "exemplo",
  "transcricao": "transcrição do áudio",
  "gemini_resposta": {
    "avaliacao": "correta",
    "justificativa": "A pronúncia foi clara e natural.",
    "correcao_sugerida": null
  },
  "openai_resposta": {
    "avaliacao": "aceitável",
    "justificativa": "A palavra foi pronunciada com sotaque, mas inteligível.",
    "correcao_sugerida": null,
    "nivel_confianca": 0.85
  }
}
```

## Dependências

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Google Generative AI](https://developers.generativeai.google/)
- [Rich](https://github.com/Textualize/rich)
- [Python Dotenv](https://github.com/theskumar/python-dotenv)

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.