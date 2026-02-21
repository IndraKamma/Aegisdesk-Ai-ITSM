from fastapi import APIRouter
from app.schemas.ai import AITriageRequest, AITriageResponse
from app.services.ai_service import triage

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/triage", response_model=AITriageResponse)
def ai_triage(payload: AITriageRequest):
    summary, category, priority, assign = triage(payload.title, payload.description)
    return AITriageResponse(
        summary=summary,
        category=category,
        priority=priority,
        assignment_suggestion=assign,
    )