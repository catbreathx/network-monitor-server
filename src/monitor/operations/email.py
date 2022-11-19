from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


class EmailNotification:
    def send_email(self, message: MessageSchema, configuration: ConnectionConfig):
        fastmail = self._create_configuration(configuration)
        fastmail.send_message(message)

    def _create_configuration(self, configuration: ConnectionConfig) -> FastMail:
        fast_mail = FastMail(configuration)
        return fast_mail
