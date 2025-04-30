from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjecModel import ProjectModel
from helpers import get_db, Database
from models.db_schemes import DataChunk, Asset
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from bson import ObjectId
from models.enums import AssetTypeEnum




logger = logging.getLogger("uvicorn.errors")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    db_client: Database = Depends(get_db),
    app_settings: Settings = Depends(get_settings),
):
    data_obj = DataController()
    # validate the file properties 
    is_valid, result_signal = data_obj.validate_uploaded_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )
    
    project_model = ProjectModel(
        db_client=db_client
    )
    
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    
    file_path, file_id = data_obj.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id    
    )
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
                
    except Exception as e:
        logger.error(f"Error wile uploading file: {e}")
        return JSONResponse(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                    "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )
    
    # store the assets into the database
    
    asset_model = AssetModel(db_client=db_client)
    
    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    
    asset_record = await asset_model.create_asset(asset=asset_resource)
        
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": str(asset_record.id),
        }
    )
    
    
@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str, 
    process_request: ProcessRequest,
    db_client: Database = Depends(get_db)
):
    
    # file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    
    
    project_model = ProjectModel(
        db_client=db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )  
    
    asset_model = AssetModel(db_client=db_client)
    
    assets_for_project = await asset_model.get_all_assets_by_project_id(asset_project_id=project.id)
     
    process_controller = ProcessController(project_id=project_id)
    
    all_file_chunks = [] 
    
    for asset in assets_for_project:
        file_content = process_controller.get_file_content(file_id=asset.asset_name)
        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id= asset.asset_name,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )
        
        if file_chunks:
                all_file_chunks.extend(file_chunks)
        
    
    if not all_file_chunks or len(all_file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )
        
    file_chunks_records = [
        DataChunk(
            chunk_text= chunk.page_content,
            chunk_metadata= chunk.metadata,
            chunk_project_id=ObjectId(project.id),
            chunk_order=chunk.id
        )
        for chunk in all_file_chunks
    ]
    
    chunk_model = ChunkModel(db_client=db_client)
    
    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )
    
    no_of_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_of_records,
        }
    ) 