from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

# IMPORTANT: import models so SQLAlchemy registers tables
from app.models.ticket import Ticket  # noqa
from app.models.comment import Comment  # noqa
from app.models.audit_log import AuditLog  # noqa

from app.api.routes.tickets import router as tickets_router
from app.api.routes.comments import router as comments_router
from app.api.routes.ai import router as ai_router


# FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None,
    redoc_url=None,
)


BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")


def _tpl(name: str) -> str:
    return (WEB_DIR / "templates" / name).read_text(encoding="utf-8")


# MAIN WELCOME PAGE
@app.get("/", response_class=HTMLResponse)
def welcome_page():
    return _tpl("welcome.html")


# ABOUT PAGE
@app.get("/about", response_class=HTMLResponse)
def about_page():
    return _tpl("about.html")


# SERVICES PAGE
@app.get("/services", response_class=HTMLResponse)
def services_page():
    return _tpl("services.html")


# RECORDS PAGE
@app.get("/records", response_class=HTMLResponse)
def records_page():
    return _tpl("records.html")


# API DOCS (styled)
from fastapi.responses import HTMLResponse

@app.get("/docs", include_in_schema=False)
def custom_docs():
    html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.APP_NAME} — API Docs",
        swagger_css_url="/static/swagger-dark.css",
    ).body.decode("utf-8")

    back_button = """
    <div class="docs-back">
        <a href="/" class="btn">← Back to Home</a>
    </div>

    <style>
    .docs-back {
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 9999;
    }

    .docs-back .btn {
        background: #38bdf8;
        color: #0f172a;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 600;
        text-decoration: none;
        transition: 0.2s;
    }

    .docs-back .btn:hover {
        background: #0ea5e9;
        color: white;
    }
    </style>
    """

    html = html.replace("<body>", "<body>" + back_button)

    return HTMLResponse(html)


# HEALTH CHECK
@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}


# CREATE TABLES
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# API ROUTERS
app.include_router(tickets_router, prefix=settings.API_PREFIX)
app.include_router(comments_router, prefix=settings.API_PREFIX)
app.include_router(ai_router, prefix=settings.API_PREFIX)