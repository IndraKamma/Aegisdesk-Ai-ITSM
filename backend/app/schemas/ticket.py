from pydantic import BaseModel, Field
from datetime import datetime

class TicketCreate(BaseModel):
    requester_name: str = Field(min_length=1, max_length=120)
    requester_email: str | None = None
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    category: str = "General"
    priority: str = "Medium"

class TicketUpdate(BaseModel):
    category: str | None = None
    priority: str | None = None
    status: str | None = None
    assigned_to: str | None = None

class TicketOut(BaseModel):
    id: int
    requester_name: str
    requester_email: str | None
    title: str
    description: str
    category: str
    priority: str
    status: str
    assigned_to: str | None
    sla_minutes: int
    due_by: datetime | None
    ai_summary: str | None
    ai_assignment_suggestion: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True