from typing import List
from typing import Any
from dataclasses import dataclass

@dataclass
class Record:
    id: str
    permissionType: str
    status: str
    activity: str
    dutyHolder: str
    suburb: str
    postcode: str

    @staticmethod
    def from_dict(obj: Any) -> 'Record':
        _id = str(obj.get("id"))
        _permissionType = str(obj.get("permissionType"))
        _status = str(obj.get("status"))
        _activity = str(obj.get("activity"))
        _dutyHolder = str(obj.get("dutyHolder"))
        _suburb = str(obj.get("suburb"))
        _postcode = str(obj.get("postcode"))
        return Record(_id, _permissionType, _status, _activity, _dutyHolder, _suburb, _postcode)

@dataclass
class PlanningPermissions:
    total: int
    permissions: List[Record]
    page: int
    pageSize: int

    @staticmethod
    def from_dict(obj: Any) -> 'PlanningPermissions':
        _total = int(obj.get("total"))
        _permissions = [Record.from_dict(y) for y in obj.get("records")]
        _page = int(obj.get("page"))
        _pageSize = int(obj.get("pageSize"))
        return PlanningPermissions(_total, _permissions, _page, _pageSize)