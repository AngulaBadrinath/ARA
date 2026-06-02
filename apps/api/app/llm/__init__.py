"""LLM provider abstraction — implement concrete providers in submodules."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def analyze_resume(self, resume_text: str, job_description: str | None = None) -> dict:
        """Return structured analysis JSON."""
        ...


class OllamaProvider(LLMProvider):
    async def analyze_resume(self, resume_text: str, job_description: str | None = None) -> dict:
        raise NotImplementedError


def get_llm_provider() -> LLMProvider:
    from app.core.config import get_settings

    settings = get_settings()
    if settings.llm_provider == "ollama":
        return OllamaProvider()
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
