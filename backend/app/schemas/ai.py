from pydantic import BaseModel, Field

class AITriageRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

class AITriageResponse(BaseModel):
    summary: str
    category: str
    priority: str
    assignment_suggestion: str