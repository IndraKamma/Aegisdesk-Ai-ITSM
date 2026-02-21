# 🛡️ AegisDesk AI ITSM

### AI-Powered IT Service Management System for Data Center & Network Operations 🚀

---

# 🚀 Overview

AegisDesk AI is a modern, scalable IT Service Management (ITSM) platform designed to simulate real-world Data Center and Network Operations workflows.

The system enables IT teams to efficiently manage incident tickets, assign technicians, track resolution status, and leverage AI-ready infrastructure for intelligent incident triage and automation.

Built using FastAPI, PostgreSQL, Docker, and a custom dashboard UI, the platform follows production-grade backend architecture and infrastructure design patterns.

---

# 🔎 Core Capabilities

✔ Incident ticket creation and lifecycle management
✔ Technician assignment and resolution tracking
✔ Solved vs Unsolved incident monitoring
✔ Operational records dashboard
✔ REST API powered backend (FastAPI)
✔ PostgreSQL database with scalable schema design
✔ Docker-based infrastructure deployment
✔ AI-ready architecture with embedding and triage support

---

# 🏗 System Architecture

```
User Interface (Dashboard)
        ↓
FastAPI Backend (REST API)
        ↓
Business Logic Layer
        ↓
SQLAlchemy ORM
        ↓
PostgreSQL Database (pgvector enabled)
        ↓
Docker Infrastructure
```

Optional AI Layer:

```
Incident Ticket
     ↓
Embedding Service
     ↓
Vector Database (pgvector)
     ↓
AI Triage / Analysis Engine
```

---

# 🧱 Tech Stack

## Backend

• FastAPI
• Python
• SQLAlchemy ORM
• Pydantic

## Database

• PostgreSQL
• pgvector (vector search ready)

## Frontend

• HTML
• CSS
• JavaScript
• Custom Dashboard UI

## Infrastructure

• Docker
• Docker Compose
• NGINX

## AI / Future Integration

• Ollama support ready
• Embedding service ready
• Vector search ready

---

# 📂 Project Structure

```
AegisDesk-AI-ITSM/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── web/
│   │   │   ├── static/
│   │   │   └── templates/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│
├── infra/
│   ├── docker-compose.yml
│   ├── postgres/
│   └── nginx/
│
└── docs/
```

---

# ⚙ ITSM Workflow

## Ticket Creation

User submits incident ticket:

```
POST /api/tickets
```

Stored in PostgreSQL database.

---

## Ticket Management

Technicians can:

• View all tickets
• Filter solved / unsolved tickets
• Assign technician name
• Mark ticket as solved

---

## Records Dashboard

Displays:

• All tickets
• Ticket status
• Technician assignment
• Resolution tracking

---

# 🤖 AI-Ready Architecture

System includes foundation for:

• AI incident triage
• Semantic search
• Vector embeddings
• Intelligent incident recommendations

---

# 📊 Dashboard & UI

## Welcome Page

![Screenshot_21-2-2026_15229_127 0 0 1](https://github.com/user-attachments/assets/be2ba901-c6f9-4851-b113-093c0608fede)


## Records Dashboard
![Screenshot_21-2-2026_153452_127 0 0 1](https://github.com/user-attachments/assets/d7b1bd29-6a93-4bb5-ab1e-26277f942b46)



## API Docs Interface

![Screenshot_21-2-2026_153044_127 0 0 1](https://github.com/user-attachments/assets/37358f98-00f7-40f2-9f5d-2cdb948fcf4b)

---

# 💼 Business Value

This system demonstrates real-world ITSM capabilities used in:

• Data Centers
• Cloud Infrastructure Teams
• Network Operations Centers (NOC)
• IT Support Organizations

Business Impact:

✔ Faster incident resolution
✔ Improved operational visibility
✔ Technician accountability
✔ Scalable backend architecture
✔ AI-ready incident automation

---

# ▶️ How To Run

## 1. Start Database

```
cd infra
docker compose up -d
```

---

## 2. Start Backend

```
cd backend
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

---

## 3. Open Application

```
http://127.0.0.1:8000
```

---

## 4. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

# 📈 Engineering Highlights

✔ Production-grade backend architecture
✔ REST API design with FastAPI
✔ PostgreSQL database integration
✔ Docker infrastructure deployment
✔ Modular service-based backend design
✔ Scalable ITSM data model
✔ AI-ready system architecture

---

# 🚀 Future Improvements

• AI incident auto-classification
• Technician workload optimization
• Authentication & RBAC
• Live dashboard updates
• Kubernetes deployment
• Cloud deployment (AWS / Azure)

---

# 👨‍💻 Author

Indra Sairam Kumar Kamma
Master of Science, Computer Science
University of Memphis

GitHub:
[https://github.com/IndraKamma](https://github.com/IndraKamma)

---

