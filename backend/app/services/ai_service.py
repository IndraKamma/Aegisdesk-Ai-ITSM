import re
import requests
from app.core.config import settings

CATEGORIES = ["Network", "Hardware", "Access", "Software", "Security", "General"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]

def _heuristic_triage(title: str, description: str):
    text = f"{title} {description}".lower()

    # Category rules
    if any(k in text for k in ["switch", "router", "packet", "latency", "ping", "dns", "ip", "bgp", "ospf", "vlan"]):
        category = "Network"
    elif any(k in text for k in ["disk", "ssd", "hdd", "fan", "power", "psu", "ram", "server down", "rack"]):
        category = "Hardware"
    elif any(k in text for k in ["password", "locked", "access", "vpn", "login", "mfa", "account"]):
        category = "Access"
    elif any(k in text for k in ["malware", "phishing", "breach", "unauthorized", "ransomware"]):
        category = "Security"
    elif any(k in text for k in ["install", "crash", "bug", "error", "application", "service failed"]):
        category = "Software"
    else:
        category = "General"

    # Priority rules
    if any(k in text for k in ["outage", "down", "sev1", "critical", "production down", "p1"]):
        priority = "Critical"
    elif any(k in text for k in ["major", "high", "sev2", "p2"]):
        priority = "High"
    elif any(k in text for k in ["slow", "intermittent", "minor"]):
        priority = "Medium"
    else:
        priority = "Medium"

    # Assignment suggestion
    if category == "Network":
        assign = "Network Technician"
    elif category == "Hardware":
        assign = "Data Center Technician"
    elif category == "Access":
        assign = "IT Support"
    elif category == "Security":
        assign = "Security Analyst"
    elif category == "Software":
        assign = "Systems/Application Support"
    else:
        assign = "Service Desk"

    summary = (description.strip()[:220] + ("..." if len(description.strip()) > 220 else "")).strip()
    return summary, category, priority, assign

def triage(title: str, description: str):
    """
    Works in 2 modes:
    1) If Ollama is running, use LLM.
    2) Otherwise, use strong heuristics (still impressive for demos).
    """
    # Try Ollama (optional)
    try:
        prompt = (
            "You are an ITSM triage assistant. Return ONLY JSON with keys: "
            "summary, category, priority, assignment_suggestion.\n\n"
            f"Title: {title}\nDescription: {description}\n\n"
            f"Allowed category: {CATEGORIES}\nAllowed priority: {PRIORITIES}\n"
        )
        r = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={"model": "llama3.1", "prompt": prompt, "stream": False},
            timeout=5,
        )
        if r.ok:
            txt = r.json().get("response", "")
            # Extract JSON object if model includes extra text
            m = re.search(r"\{.*\}", txt, re.S)
            if m:
                import json
                data = json.loads(m.group(0))
                return (
                    data.get("summary", ""),
                    data.get("category", "General"),
                    data.get("priority", "Medium"),
                    data.get("assignment_suggestion", "Service Desk"),
                )
    except Exception:
        pass

    return _heuristic_triage(title, description)