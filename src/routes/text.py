from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import logging
from helpers.config import get_settings, Settings
from helpers.factories import get_llm_clients

logger = logging.getLogger("uvicorn.errors")

text_router = APIRouter(
    prefix="/api/v1/text",
    tags=["api_v1", "text"],
)

# Define a Pydantic model for the request data
class GenerateRequest(BaseModel):
    prompt: str
    action: str  # Action could be 'generate' for text generation or 'embed' for embeddings


@text_router.post("/generate")
async def upload_data(
    request: GenerateRequest,
    llm_clients: tuple = Depends(get_llm_clients),
):
    generation_client, embedding_client = llm_clients
    
    # Based on the action, either generate text or return embeddings
    try:
        if request.action == "generate":
            logger.info(f"Generating text for prompt: {request.prompt}")
            generated_text = generation_client.generate_text(
                prompt=request.prompt
            )
            if not generated_text:
                raise HTTPException(status_code=500, detail="Text generation failed.")
            return {"generated_text": generated_text}
        
        elif request.action == "embed":
            logger.info(f"Generating embedding for text: {request.prompt}")
            embedding = embedding_client.embed_text(text=request.prompt)
            if not embedding:
                raise HTTPException(status_code=500, detail="Text embedding failed.")
            return {"embedding": embedding}
        
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Must be 'generate' or 'embed'.")
    
    except Exception as e:
        logger.error(f"Error in /generate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")