import smtplib
from email.mime.text import MIMEText
from datetime import datetime


class Notifier:
    def __init__(self, config=None):
        """
        config: dictionary containing optional configs like:
        {
            "email": {
                "enabled": True,
                "sender": "...",
                "password": "...",
                "receiver": "...",
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587
            },
            "sms": {
                "enabled": False
            },
            "console": True
        }
        """
        self.config = config or {}

    # -------------------------
    # PUBLIC METHOD (MAIN ENTRY)
    # -------------------------
    def send_alert(self, alert_data: dict):
        """
        Main function to trigger notifications.
        This is what alert_system.py will call.
        """
        formatted_msg = self._format_message(alert_data)

        # Console alert (always useful for debugging)
        if self.config.get("console", True):
            self._send_console(formatted_msg)

        # Email alert
        if self.config.get("email", {}).get("enabled", False):
            self._send_email(formatted_msg)

        # SMS alert (placeholder)
        if self.config.get("sms", {}).get("enabled", False):
            self._send_sms(formatted_msg)

    # -------------------------
    # MESSAGE FORMATTER
    # -------------------------
    def _format_message(self, alert_data: dict) -> str:
        """
        Convert alert dictionary into readable message.
        Flexible to handle missing keys.
        """
        timestamp = alert_data.get(
            "timestamp",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        risk = alert_data.get("risk_level", "UNKNOWN")
        zone = alert_data.get("zone_id", "N/A")
        density = alert_data.get("density", "N/A")
        message = alert_data.get("message", "No message provided")

        formatted = (
            f"[ALERT]\n"
            f"Time      : {timestamp}\n"
            f"Risk Level: {risk}\n"
            f"Zone      : {zone}\n"
            f"Density   : {density}\n"
            f"Message   : {message}\n"
        )

        return formatted

    # -------------------------
    # CONSOLE ALERT
    # -------------------------
    def _send_console(self, message: str):
        print("\n" + "=" * 50)
        print(message)
        print("=" * 50 + "\n")

    # -------------------------
    # EMAIL ALERT
    # -------------------------
    def _send_email(self, message: str):
        try:
            email_cfg = self.config.get("email", {})

            msg = MIMEText(message)
            msg["Subject"] = "🚨 Crowd Alert Notification"
            msg["From"] = email_cfg["sender"]
            msg["To"] = email_cfg["receiver"]

            server = smtplib.SMTP(
                email_cfg.get("smtp_server", "smtp.gmail.com"),
                email_cfg.get("smtp_port", 587)
            )
            server.starttls()
            server.login(email_cfg["sender"], email_cfg["password"])
            server.send_message(msg)
            server.quit()

            print("✅ Email alert sent")

        except Exception as e:
            print(f"❌ Email alert failed: {e}")

    # -------------------------
    # SMS ALERT (PLACEHOLDER)
    # -------------------------
    def _send_sms(self, message: str):
        """
        Placeholder for SMS integration (Twilio, etc.)
        """
        print("📱 SMS alert (not implemented yet)")
        print(message)


# -------------------------
# TESTING (RUN THIS FILE DIRECTLY)
# -------------------------
if __name__ == "__main__":
    sample_alert = {
        "risk_level": "HIGH",
        "zone_id": 2,
        "density": 6.2,
        "message": "Critical crowd buildup detected"
    }

    config = {
        "console": True,
        "email": {
            "enabled": False,  # Turn True when ready
            "sender": "your_email@gmail.com",
            "password": "your_password",
            "receiver": "receiver@gmail.com"
        },
        "sms": {
            "enabled": False
        }
    }

    notifier = Notifier(config)
    notifier.send_alert(sample_alert)