# azure-ai-python-labs

Laboratório de análise de sentimento com a API Azure AI Text Analytics.

O script `src/main.py` envia frases para o serviço de sentimento do Azure e imprime o resultado de cada uma. Se `AZURE_AI_ENDPOINT` ou `AZURE_AI_KEY` estiver ausente, vazio ou ainda com o valor de exemplo de `.env.example`, o script entra em **modo simulação**: registra um aviso e imprime um resultado no mesmo formato, sem chamar a rede.

## Configuração

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copie o exemplo e preencha o endpoint e a chave do seu recurso Azure:

```bash
cp .env.example .env
```

```
AZURE_AI_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/
AZURE_AI_KEY=sua_chave_de_api_aqui
```

## Execução

```bash
python3 src/main.py
```

Para cada frase, o script imprime:

- o texto
- o sentimento: `POSITIVO`, `NEUTRO` ou `NEGATIVO`
- as pontuações de confiança `Positive`, `Neutral` e `Negative`

O arquivo `.env` está no `.gitignore` e não deve ser commitado. Use apenas os placeholders de `.env.example` no repositório.
