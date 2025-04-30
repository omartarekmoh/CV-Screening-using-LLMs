from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


class AssetModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorClient):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
        
    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.model_dump(by_alias=True))
        asset.id = result.inserted_id
        return asset
    
    async def get_all_assets_by_project_id(self, asset_project_id: str):
        result = await self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id
        }).to_list(length=None)
        
        if result is None:
            return None
        
        return [Asset(**asset) for asset in result]
