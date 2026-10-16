"""Offline GoHighLevel-style CRM workflow demo. No live GHL API calls."""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

PIPELINE_STAGES = ("New Lead", "Contacted", "Appointment Booked", "Won", "Lost")

@dataclass
class Lead:
    contact_id: str
    name: str
    email: str
    phone: str
    service: str
    stage: str = "New Lead"
    opted_out: bool = False


def normalize_lead(payload: dict) -> Lead:
    """Validate an illustrative lead-capture webhook payload."""
    required = ("contact_id", "name", "email", "phone", "service")
    missing = [key for key in required if not str(payload.get(key, "")).strip()]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", str(payload["email"])):
        raise ValueError("Invalid email format")
    return Lead(**{k: str(payload[k]).strip() for k in required}, opted_out=payload.get("opted_out") is True)


def plan_actions(lead: Lead, event: str) -> dict:
    """Produce suggested CRM actions; does not contact a customer or GHL."""
    if event not in {"lead_created", "appointment_booked", "customer_replied", "deal_won"}:
        raise ValueError(f"Unsupported event: {event}")
    stage = {"lead_created": "New Lead", "appointment_booked": "Appointment Booked", "customer_replied": "Contacted", "deal_won": "Won"}[event]
    actions = [{"action": "upsert_contact", "contact_id": lead.contact_id},
               {"action": "set_pipeline_stage", "stage": stage}]
    if event == "lead_created" and not lead.opted_out:
        actions.append({"action": "queue_followup_for_review", "channel": "email", "delay_hours": 1})
    if event == "appointment_booked" and not lead.opted_out:
        actions.append({"action": "queue_appointment_reminder_for_review", "channel": "email"})
    return {"mode": "simulation_only", "event": event, "lead": asdict(lead), "actions": actions}


def process(payload: dict) -> dict:
    if not isinstance(payload, dict) or not isinstance(payload.get("contact"), dict):
        raise ValueError("Expected JSON object with a contact object")
    return plan_actions(normalize_lead(payload["contact"]), payload.get("event", "lead_created"))


if __name__ == "__main__":
    sample = Path(__file__).resolve().parents[1] / "examples" / "lead_created.json"
    print(json.dumps(process(json.loads(sample.read_text(encoding="utf-8"))), indent=2))
