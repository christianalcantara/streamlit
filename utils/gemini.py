"""Funções de acesso à API do Google Gemini."""

import os
from collections.abc import Iterator

import streamlit as st
from google import genai
from google.genai import types

MODELO_PADRAO = "gemini-3.5-flash-lite"


def _ler_secret(nome: str) -> str | None:
    """Lê de st.secrets (Streamlit Cloud) e, se não existir, da variável de ambiente."""
    try:
        valor = st.secrets.get(nome)
    except FileNotFoundError:
        valor = None
    return valor or os.getenv(nome)


def obter_modelo() -> str:
    return _ler_secret("GEMINI_MODEL") or MODELO_PADRAO


def obter_chave_api() -> str | None:
    return _ler_secret("GEMINI_API_KEY") or _ler_secret("GOOGLE_API_KEY")


@st.cache_resource(max_entries=10)
def obter_cliente(chave: str) -> genai.Client:
    """Cria o cliente uma única vez por chave (não a cada reexecução do script)."""
    return genai.Client(api_key=chave)


def para_formato_gemini(mensagens: list[dict]) -> list[types.Content]:
    """Converte o histórico do chat. No Gemini o papel da IA se chama "model"."""
    return [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in mensagens
    ]


def gerar_resposta(
    cliente: genai.Client,
    modelo: str,
    mensagens: list[dict],
    instrucao: str,
    temperatura: float,
) -> Iterator[str]:
    """Gerador que entrega a resposta pedaço por pedaço (streaming)."""
    stream = cliente.models.generate_content_stream(
        model=modelo,
        contents=para_formato_gemini(mensagens),
        config=types.GenerateContentConfig(
            system_instruction=instrucao,
            temperature=temperatura,
        ),
    )
    for pedaco in stream:
        if pedaco.text:  # alguns pedaços podem vir vazios
            yield pedaco.text
