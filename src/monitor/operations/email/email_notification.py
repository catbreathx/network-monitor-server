from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from monitor.operations.email import schema


class EmailNotification:
    _fastmail: FastMail

    def __init__(self, configuration: ConnectionConfig) -> None:
        super().__init__()
        self._fastmail = self._create_configuration(configuration)

    async def send_email(self, email: schema.EmailSchema):
        message = MessageSchema(
            subject="Health Check Report",
            recipients=email.recipients_email,
            template_body=email.dict().get("body"),
            subtype=MessageType.html,
        )

        await self._fastmail.send_message(message, template_name="healthcheck_report.html")

    def _create_configuration(self, configuration: ConnectionConfig) -> FastMail:
        fast_mail = FastMail(configuration)
        return fast_mail
