"""SMTP email dispatch step."""
from __future__ import annotations

import json
import smtplib
from email.message import EmailMessage
from typing import Any

from flowforge.app.config import settings
from flowforge.steps.base_step import BaseStep


class EmailStep(BaseStep):
    """Sends workflow data by email via SMTP."""

    def validate_config(self) -> None:
        if not self.config.get("to"):
            raise ValueError("EmailStep requires 'to' recipient")
        if not settings.smtp_host or not settings.smtp_user or not settings.smtp_password:
            raise ValueError("SMTP settings are required in environment")

    def execute(self, input_data: Any) -> dict[str, Any]:
        message = EmailMessage()
        message["Subject"] = self.config.get("subject", "FlowForge Notification")
        message["From"] = settings.smtp_sender or settings.smtp_user
        message["To"] = self.config["to"]
        message.set_content(self.config.get("body", json.dumps(input_data, indent=2, default=str)))

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as smtp:
            if settings.smtp_use_tls:
                smtp.starttls()
            smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.send_message(message)

        return {"status": "sent", "recipient": self.config["to"], "data": input_data}
