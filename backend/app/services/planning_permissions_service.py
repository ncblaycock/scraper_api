import requests
from app.models.planning_permission import PlanningPermissions

class PlanningPermissionsService:
    def __init__(self):
        pass
    
    def get_planning_permissions(self, skip: int = 0, limit: int = 100):
        results = requests.get("https://www.epa.vic.gov.au/api/public-register/permissions?permissionType=Development+licence&page=1&pageSize=1000")
        return PlanningPermissions.from_dict(results.json())