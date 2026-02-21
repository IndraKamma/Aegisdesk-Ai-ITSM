from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.audit_log import AuditLog
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from app.services.ai_service import triage

router = APIRouter(prefix="/tickets", tags=["tickets"])

def _calc_due_by(sla_minutes: int):
    return datetime.utcnow() + timedelta(minutes=sla_minutes)

@router.post("", response_model=TicketOut)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    # AI triage (summary/category/priority/suggestion)
    summary, category, priority, assign = triage(payload.title, payload.description)

    t = Ticket(
        requester_name=payload.requester_name,
        requester_email=payload.requester_email,
        title=payload.title,
        description=payload.description,
        category=payload.category if payload.category != "General" else category,
        priority=payload.priority if payload.priority else priority,
        status="Open",
        assigned_to=None,
        sla_minutes=240 if priority in ["Low", "Medium"] else 120 if priority == "High" else 60,
        due_by=None,
        ai_summary=summary,
        ai_assignment_suggestion=assign,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    t.due_by = _calc_due_by(t.sla_minutes)

    db.add(t)
    db.commit()
    db.refresh(t)

    db.add(AuditLog(entity_type="ticket", entity_id=t.id, action="created", detail=f"priority={t.priority}, category={t.category}"))
    db.commit()

    return t

@router.get("", response_model=list[TicketOut])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t

@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")

    changes = []
    if payload.category is not None:
        t.category = payload.category; changes.append(f"category={payload.category}")
    if payload.priority is not None:
        t.priority = payload.priority; changes.append(f"priority={payload.priority}")
    if payload.status is not None:
        t.status = payload.status; changes.append(f"status={payload.status}")
    if payload.assigned_to is not None:
        t.assigned_to = payload.assigned_to; changes.append(f"assigned_to={payload.assigned_to}")

    t.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(t)

    if changes:
        db.add(AuditLog(entity_type="ticket", entity_id=t.id, action="updated", detail="; ".join(changes)))
        db.commit()

    return t