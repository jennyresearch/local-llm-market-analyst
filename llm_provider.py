# llm_provider.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        from langchain_ollama.llms import OllamaLLM
        model = os.getenv("OLLAMA_MODEL", "gemma3n")
        return OllamaLLM(model=model)

    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        api_key = os.getenv("OPENAI_API_KEY")
        return ChatOpenAI(model=model, api_key=api_key)

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: '{provider}'. Use 'ollama' or 'openai'.")