from ..LLMInterface import EmbeddingInterface
import logging
import requests


class JinaAIProvider(EmbeddingInterface):
    
    def __init__(self, default_input_max_characters: int=1000, 
                    api_url: str=None,
                    api_key: str=None):
        
        self.default_input_max_characters = default_input_max_characters
        
        self.embedding_model_id = None
        self.embedding_size = None
    
        self.api_url = api_url
        self.api_key = api_key
        
        self.logger = logging.getLogger(__name__)
    
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def embed_text(self, text: str, document_type: str = None):
        if not self.embedding_api_url:
            self.logger.error("Embedding API URL isn't set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for JinaAI isn't set")
            return None
        
        response = self.send_embedding_request(text)
        
        if response.status_code != 200:
            self.logger.error(f"Error while embedding text with external model. Status code: {response.status_code}")
            return None
        
        data = response.json()
        
        if not data or not data["data"] or data["data"][0]["embedding"]:
            self.logger.error("No embedding found in the response")
            return None
        
        return data["data"][0]["embedding"]
    
    def send_embedding_request(self, text):
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(
            self.api_url,
            headers=headers,
            json={
                "model": self.embedding_model_id,
                "input": [self.process_text(text)]
            }
        )
        
        return response

