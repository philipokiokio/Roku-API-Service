from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import mail_settings, EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.mail_username,
    MAIL_PASSWORD=mail_settings.mail_password,
    MAIL_FROM=mail_settings.mail_from,
    MAIL_PORT=mail_settings.mail_port,
    MAIL_SERVER=mail_settings.mail_server,
    MAIL_FROM_NAME=mail_settings.mail_from_name,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent.parent / "templates",
)


async def send_mail(
    recieptients: EmailStr, subject: str, body: dict, template_name: str
) -> bool:

    message = MessageSchema(
        subject=subject,
        recipients=recieptients,
        template_body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)

    status = False
    try:
        await fm.send_message(message, template_name=template_name)
        status = True
    except:
        pass
    return status
