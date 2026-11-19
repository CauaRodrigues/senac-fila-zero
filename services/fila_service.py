
import json
import math
from pathlib import Path

# Localizacao do arquivo de dados
BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_CAIXAS = BASE_DIR / "data" / "caixas.json"


def carregar_caixas():
    """Carrega os caixas cadastrados no arquivo JSON."""

    with open(ARQUIVO_CAIXAS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados["caixas"]


def calcular_tempo_espera(pessoas, tempo_atendimento):
    """Calcula a estimativa de espera em minutos."""

    segundos = pessoas * tempo_atendimento
    minutos = math.ceil(segundos / 60)

    return minutos


def classificar_fila(tempo):
    """Classifica a fila de acordo com o tempo estimado."""

    if tempo <= 5:
        return "baixa"

    elif tempo <= 12:
        return "media"

    return "alta"


def consultar_caixas():
    """Retorna os caixas com suas estimativas e recomendações."""

    caixas = carregar_caixas()
    resultado = []

    for caixa in caixas:

        if not caixa["aberto"]:
            resultado.append({
                **caixa,
                "tempo_espera": None,
                "classificacao": "fechado",
                "recomendado": False
            })
            continue

        tempo = calcular_tempo_espera(
            caixa["pessoas"],
            caixa["tempo_atendimento"]
        )

        resultado.append({
            **caixa,
            "tempo_espera": tempo,
            "classificacao": classificar_fila(tempo),
            "recomendado": False
        })

    # Identifica o menor tempo entre os caixas abertos
    caixas_abertos = [
        caixa for caixa in resultado
        if caixa["classificacao"] != "fechado"
    ]

    if caixas_abertos:
        menor_tempo = min(
            caixa["tempo_espera"] for caixa in caixas_abertos
        )

        for caixa in caixas_abertos:
            if caixa["tempo_espera"] == menor_tempo:
                caixa["recomendado"] = True

    return resultado
