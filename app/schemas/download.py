from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DownloadBase(BaseModel):
    filename: str
    file_path: str
    file_size: Optional[int] = None
    content_type: Optional[str] = None

class DownloadCreate(DownloadBase):
    pass

class DownloadUpdate(BaseModel):
    filename: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None

class DownloadResponse(DownloadBase):
    id: int
    user_id: int
    download_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
