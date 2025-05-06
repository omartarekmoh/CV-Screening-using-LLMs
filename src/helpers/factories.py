from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

def get_llm_clients():
    settings = get_settings()
    llm_provider_factory = LLMProviderFactory(settings)
    generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID, embedding_size=settings.EMBEDDING_MODEL_SIZE)
    return generation_client, embedding_client