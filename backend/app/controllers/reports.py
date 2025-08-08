from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.planning_permissions_service import PlanningPermissionsService
from app.schemas.report import ReportCreate, ReportUpdate, ReportResponse
from app.auth import get_current_active_user
from app.models.user import User
from app.models.planning_permission import PlanningPermissions

router = APIRouter()

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report: ReportCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new report"""
    # TODO: Implement report creation logic
    # This is a placeholder implementation
    return {
        "id": 1,
        "title": report.title,
        "description": report.description,
        "status": report.status,
        "user_id": current_user.id,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

@router.get("/", response_model=PlanningPermissions)
def get_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get all reports for the current user"""
    # TODO: Implement report retrieval logic
    # This is a placeholder implementation
    response = PlanningPermissionsService().get_planning_permissions(skip, limit)
    return response

@router.get("/{report_id}", response_model=PlanningPermissions)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific report by ID"""
    # TODO: Implement report retrieval logic
    # This is a placeholder implementation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Report not found"
    )

@router.put("/{report_id}", response_model=PlanningPermissions)
def update_report(
    report_id: int,
    report_update: ReportUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific report"""
    # TODO: Implement report update logic
    # This is a placeholder implementation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Report not found"
    )

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a specific report"""
    # TODO: Implement report deletion logic
    # This is a placeholder implementation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Report not found"
    )
