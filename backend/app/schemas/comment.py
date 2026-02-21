from pydantic import BaseModel, Field
from datetime import datetime

class CommentCreate(BaseModel):
    author: str = Field(default="Technician", max_length=120)
    body: str = Field(min_length=1)

class CommentOut(BaseModel):
    id: int
    ticket_id: int
    author: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True