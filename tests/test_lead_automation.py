import unittest
from src.lead_automation import process

LEAD = {"contact_id": "demo-001", "name": "Sample Customer", "email": "sample@example.org", "phone": "+15550100000", "service": "Consultation"}

class DemoTests(unittest.TestCase):
    def test_new_lead_followup(self):
        result = process({"event": "lead_created", "contact": LEAD})
        self.assertEqual(result["actions"][1]["stage"], "New Lead")
        self.assertEqual(result["actions"][2]["action"], "queue_followup_for_review")

    def test_opt_out_prevents_followup(self):
        result = process({"event": "lead_created", "contact": {**LEAD, "opted_out": True}})
        self.assertEqual(len(result["actions"]), 2)

    def test_booking_updates_stage(self):
        result = process({"event": "appointment_booked", "contact": LEAD})
        self.assertEqual(result["actions"][1]["stage"], "Appointment Booked")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            process({"event": "lead_created", "contact": {**LEAD, "email": "invalid"}})

    def test_unknown_event(self):
        with self.assertRaises(ValueError):
            process({"event": "unknown", "contact": LEAD})

if __name__ == "__main__":
    unittest.main()
