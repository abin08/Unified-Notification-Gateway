from smtplib import SMTP
from email.message import EmailMessage

from app.services.base import BaseNotifier
from app.core.config import Settings
from app.schemas.notification import EmailNotification


class EmailNotifier(BaseNotifier):
    """
    Concrete implementation of the BaseNotifier for sending emails via SMTP.

    This class handles the construction of the MIME message, manages the
    SMTP connection lifecycle, and performs the actual transmission.
    It relies on the global application settings for server configuration.
    """

    def __init__(self, config: Settings):
        self.config = config

    def send(self, notification: EmailNotification):
        """
        Constructs and sends an email based on the provided
        notification payload.

        This method connects to the SMTP server configured in settings,
        upgrades the connection to TLS for security, authenticates, and
        dispatches the message.

        Args:
            notification (EmailNotification): The validated email request
                                              object containing recipient
                                              lists (to, cc, bcc),
                                              subject, and HTML body content.

        Raises:
            SMTPException: If the SMTP server returns an error
                            (connection failed, authentication failed,
                             or recipient rejected).
            ConnectionRefusedError: If the server cannot be reached.
        """
        msg = EmailMessage()
        msg["Subject"] = notification.content.subject
        msg["From"] = self.config.EMAILS_FROM_EMAIL

        # Convert list of emails to comma-separated string for headers
        msg["To"] = ", ".join(notification.recipient.to)
        if notification.recipient.cc:
            msg["Cc"] = ", ".join(notification.recipient.cc)
        if notification.recipient.bcc:
            msg["Bcc"] = ", ".join(notification.recipient.bcc)

        # Set the body
        msg.set_content(
            notification.content.html_body,
            subtype="html"
        )

        # Send email via SMTP. Context manager handles
        # the connection and quit automatically
        with SMTP(
            self.config.SMTP_SERVER,
            self.config.SMTP_PORT
        ) as server:
            # Security: Call server.starttls() to upgrade the connection.
            server.starttls()
            # Auth: Call server.login(...) using the user/password.
            server.login(
                self.config.SMTP_USER,
                self.config.SMTP_PASSWORD
            )
            # Send the email
            server.send_message(msg)
