import logging
import os

import azure.ai.textanalytics
import azure.core.credentials
import azure.core.exceptions
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ENDPOINT_PLACEHOLDER = "https://seu-recurso.cognitiveservices.azure.com/"
KEY_PLACEHOLDER = "sua_chave_de_api_aqui"

SENTIMENT_LABELS = {
    "positive": "POSITIVO",
    "neutral": "NEUTRO",
    "negative": "NEGATIVO",
}


class ClienteSimulacao:
    """Stand-in local. analisar_textos usa este objeto sem chamar o Azure."""

    simulacao = True


def _ausente_ou_placeholder(valor, placeholder):
    if valor is None:
        return True
    texto = valor.strip()
    return texto == "" or texto == placeholder


def get_client():
    endpoint = os.getenv("AZURE_AI_ENDPOINT")
    chave = os.getenv("AZURE_AI_KEY")
    if _ausente_ou_placeholder(endpoint, ENDPOINT_PLACEHOLDER) or _ausente_ou_placeholder(
        chave, KEY_PLACEHOLDER
    ):
        logger.warning(
            "Credenciais do Azure ausentes, vazias ou ainda no valor de exemplo. "
            "A execução está em modo simulação."
        )
        return ClienteSimulacao()

    return azure.ai.textanalytics.TextAnalyticsClient(
        endpoint=endpoint,
        credential=azure.core.credentials.AzureKeyCredential(chave),
    )


def _rotulo_sentimento(sentimento, positive, neutral, negative):
    rotulo = SENTIMENT_LABELS.get(str(sentimento).lower())
    if rotulo:
        return rotulo
    scores = {"POSITIVO": positive, "NEUTRO": neutral, "NEGATIVO": negative}
    return max(scores, key=scores.get)


def _imprimir_resultado(texto, sentimento, positive, neutral, negative):
    print(f"Texto: {texto}")
    print(f"Sentimento: {_rotulo_sentimento(sentimento, positive, neutral, negative)}")
    print(f"Positive: {positive:.4f}")
    print(f"Neutral: {neutral:.4f}")
    print(f"Negative: {negative:.4f}")


def _resultado_simulado(texto):
    texto_lower = texto.lower()
    negativos = ("péssim", "ruim", "horr", "atras", "triste", "problema", "pior")
    positivos = ("excelente", "feliz", "ótim", "otim", "bom", "adorei", "maravilh", "gostei")
    if any(trecho in texto_lower for trecho in negativos):
        return "negative", 0.07, 0.13, 0.80
    if any(trecho in texto_lower for trecho in positivos):
        return "positive", 0.86, 0.10, 0.04
    return "neutral", 0.15, 0.70, 0.15


def analisar_textos(client, textos):
    if getattr(client, "simulacao", False):
        for texto in textos:
            sentimento, positive, neutral, negative = _resultado_simulado(texto)
            _imprimir_resultado(texto, sentimento, positive, neutral, negative)
            print()
        return

    try:
        resultados = client.analyze_sentiment(textos, language="pt")
    except (
        azure.core.exceptions.ServiceRequestError,
        azure.core.exceptions.ServiceResponseError,
        ConnectionError,
        TimeoutError,
        OSError,
    ) as erro:
        print(
            "Não foi possível conectar ao Azure Text Analytics. "
            f"Verifique a rede e o endpoint. Detalhe: {erro}"
        )
        return

    for texto, resultado in zip(textos, resultados):
        if getattr(resultado, "is_error", False):
            print(f"Texto: {texto}")
            print(
                "Não foi possível analisar este texto: "
                f"{resultado.error.code} - {resultado.error.message}"
            )
            print()
            continue
        scores = resultado.confidence_scores
        _imprimir_resultado(
            texto,
            resultado.sentiment,
            scores.positive,
            scores.neutral,
            scores.negative,
        )
        print()


if __name__ == "__main__":
    frases = [
        "O atendimento foi excelente e fiquei muito feliz com o resultado.",
        "A entrega atrasou e a experiência foi péssima.",
    ]
    analisar_textos(get_client(), frases)
