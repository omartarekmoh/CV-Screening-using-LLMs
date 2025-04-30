from models.AssetModel import AssetModel
from controllers import ProcessController
from models.enums import AssetTypeEnum
from bson import ObjectId
from models.db_schemes import DataChunk
import logging

logger = logging.getLogger("uvicorn.errors")

async def _get_project_file_ids(asset_model: AssetModel, project_id: str, file_id: str):
    """Helper function to get file assets for a project."""
    if file_id:
        asset_for_project = await asset_model.get_asset_by_project_id_and_name(
            asset_project_id=project_id,
            asset_name=file_id
        )
        if not asset_for_project:
            return None
        return [asset_for_project]
    else:
        return await asset_model.get_all_assets_by_project_id(
            asset_project_id=project_id,
            asset_type=AssetTypeEnum.FILE.value
        )


async def _process_files(process_controller: ProcessController, project_file_ids, chunk_size, overlap_size):
    """Helper function to process file content and generate chunks."""
    all_file_chunks = []
    for asset in project_file_ids:
        file_content = process_controller.get_file_content(file_id=asset.asset_name)
        if not file_content:
            logger.error(f"Asset {asset.asset_name} not found!")
            continue

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=asset.id,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )
        
        if file_chunks:
            all_file_chunks.extend(file_chunks)
    return all_file_chunks


def _prepare_chunk_records(all_file_chunks, project_id):
    """Helper function to prepare chunk records."""
    return [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_project_id=ObjectId(project_id),
            chunk_order=chunk.id,
            chunk_asset_id=chunk.metadata["chunk_asset_id"]
        )
        for chunk in all_file_chunks
    ]
