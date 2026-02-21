from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentOut

router = APIRouter(prefix="/tickets/{ticket_id}/comments", tags=["comments"])

@router.post("", response_model=CommentOut)
def add_comment(ticket_id: int, payload: CommentCreate, db: Session = Depends(get_db)):
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")

    c = Comment(ticket_id=ticket_id, author=payload.author, body=payload.body)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("", response_model=list[CommentOut])
def list_comments(ticket_id: int, db: Session = Depends(get_db)):
    t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return db.query(Comment).filter(Comment.ticket_id == ticket_id).order_by(Comment.created_at.asc()).all()