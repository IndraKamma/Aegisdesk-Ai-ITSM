from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    requester_name: Mapped[str] = mapped_column(String(120), nullable=False)
    requester_email: Mapped[str | None] = mapped_column(String(200), nullable=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str] = mapped_column(String(50), nullable=False, default="General")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="Medium")  # Low/Medium/High/Critical
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Open")      # Open/In Progress/Resolved/Closed

    assigned_to: Mapped[str | None] = mapped_column(String(120), nullable=True)  # later: FK to users

    sla_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=240)
    due_by: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_assignment_suggestion: Mapped[str | None] = mapped_column(String(120), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")