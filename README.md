
![GoHighLevel Tests](https://github.com/hamadliaqat682/gohighlevel-crm-automation/actions/workflows/tests.yml/badge.svg)


# GoHighLevel CRM & Sales Automation — Demo

A portfolio-grade **offline demonstration** of a service-business lead automation pipeline. It illustrates lead intake, input validation, pipeline updates, appointment handling, and consent-aware follow-up planning.

> **Demo only.** This repository is not a connected GoHighLevel account, an exported GHL workflow, or a production-ready integration. It performs no outbound messages, CRM writes, or live API requests. All customer data is fictional.

## Business workflow

1. A lead form or booking event supplies contact data.
2. The processor validates and normalizes the contact.
3. Business rules choose a suggested sales pipeline stage.
4. Follow-ups are queued for review only when the contact has not opted out.
5. A CRM-ready *illustrative* JSON plan is produced.

## Features

- Lead validation, including required fields and basic email syntax
- Example pipeline stages: New Lead → Contacted → Appointment Booked → Won
- Appointment-based stage updates
- Follow-up suggestions with opt-out suppression
- 5 automated Python tests
- No third-party package installation required

## Run locally

Requires Python 3.10+.

```bash
python -m src.lead_automation
python -m unittest discover -s tests -v
```

## Example output

```json
{
  "mode": "simulation_only",
  "event": "lead_created",
  "actions": [
    {"action": "upsert_contact", "contact_id": "demo-001"},
    {"action": "set_pipeline_stage", "stage": "New Lead"},
    {"action": "queue_followup_for_review", "channel": "email", "delay_hours": 1}
  ]
}
```

The real program also returns normalized `lead` information; the example above is abbreviated.

## Files

- `src/lead_automation.py` — validation and simulated automation rules
- `tests/test_lead_automation.py` — unit tests
- `examples/` — fictional lead and appointment events
- `docs/architecture.md` — process diagram and live-integration notes

## For a production deployment

Use official GoHighLevel documentation and an authorized account; implement OAuth/API authentication, real endpoint mapping, webhook signature checks where supported, retry/idempotency handling, audit logging, and legally compliant consent/opt-out controls. Never store tokens or client data in a public repository.

## Portfolio disclaimer

This is an original technical demonstration illustrating GoHighLevel-style CRM automation concepts. It does not represent a deployed client integration or proven revenue gains.
