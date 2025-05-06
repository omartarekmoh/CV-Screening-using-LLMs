from abc import ABC, abstractmethod

class TextGenerationInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id: str):
        """
        Set the model to be used for text generation.
        """
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None, temperature: float = None):
        """
        Generate text based on the provided prompt and chat history.
        """
        pass
    
    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        """
        Construct a prompt to send to the model.
        """
        pass

class EmbeddingInterface(ABC):
    
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Set the model to be used for generating text embeddings.
        """
        pass
    
    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        """
        Embed the input text and return its vector representation.
        """
        pass
