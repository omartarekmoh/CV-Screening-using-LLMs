from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if(DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections):
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            
    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump(by_alias=True))
        project.id = result.inserted_id
        return project
    
    async def get_project_or_create_one(self, project_id: int):
        # Try to find the project by project_id in the collection
        record = await self.collection.find_one({
            "project_id": project_id
        })
        
        
        if record is None:
            # If no record is found, create a new project instance
            project = Project(project_id=project_id)
            
            # Create the new project in the database
            project = await self.create_project(project=project)
            
            # You may want to return the project after it's created
            return project

        # If the record is found, return the project data from the database
        return Project(**record)

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        # Get the total number of projects in the collection
        total_projects = await self.collection.count_documents({})
        
        # Calculate the total number of pages
        total_pages = (total_projects + page_size - 1) // page_size
        
        # Calculate the skip based on the current page and page size
        skip = (page - 1) * page_size
        
        # Use the skip and limit to fetch the projects from MongoDB
        projects_cursor = self.collection.find().skip(skip).limit(page_size)
        
        projects = []
        # Fetch all the projects from the cursor
        async for project in projects_cursor:
            projects.append(
                Project(**project)
            )
        
        return projects, total_pages

        