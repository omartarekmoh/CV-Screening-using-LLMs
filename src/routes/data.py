from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjecModel import ProjectModel
from helpers import get_db, Database
from models.db_schemes import Asset
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
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

from services.processing_service import _get_project_file_ids, _process_files, _prepare_chunk_records

@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str, 
    process_request: ProcessRequest,
    db_client: Database = Depends(get_db)
):
    # Extract the necessary fields from process_request
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    file_id = process_request.file_id

    # Initialize ProjectModel and fetch or create the project
    project_model = ProjectModel(db_client=db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Initialize AssetModel and prepare file assets
    asset_model = AssetModel(db_client=db_client)
    project_file_ids = await _get_project_file_ids(asset_model, project.id, file_id)
    
    # Handle case when no files are found
    if not project_file_ids:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.ASSET_NOT_FOUND.value},
        )

    # Initialize ProcessController and process each file
    process_controller = ProcessController(project_id=project_id)
    all_file_chunks = await _process_files(process_controller, project_file_ids, chunk_size, overlap_size)

    # Handle case when processing failed
    if not all_file_chunks:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILED.value},
        )

    # Prepare and insert chunk records
    file_chunks_records = _prepare_chunk_records(all_file_chunks, project.id)
    chunk_model = ChunkModel(db_client=db_client)

    # Reset chunks if required
    if do_reset:
        await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    # Insert new chunks
    no_of_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_of_records,
            "processed_files": len(project_file_ids)
        }
    )
