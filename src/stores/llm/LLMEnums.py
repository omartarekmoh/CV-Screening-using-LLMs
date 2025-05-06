from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    GROQ = "GROQ"
    JINAAI = "JINAAI"
     
class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    
class JinaAIEnums(Enum):
    TEXT = "text"
    IMAGE = "image"