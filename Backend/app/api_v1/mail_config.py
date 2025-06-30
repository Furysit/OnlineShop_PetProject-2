from fastapi_mail import ConnectionConfig





conf = ConnectionConfig(
    MAIL_USERNAME="9ujuxusw3sw73dqn",
    MAIL_PASSWORD="dbsysahqtlk4jkgm",
    MAIL_FROM="9ujuxusw3sw73dqn@mailmug.net",  # Почта должна совпадать с доменом
    MAIL_PORT=2525,
    MAIL_SERVER="smtp.mailmug.net",
    MAIL_FROM_NAME="Your Shop",
    MAIL_STARTTLS=True,       # Обязательно указать
    MAIL_SSL_TLS=False,       # Обязательно указать
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
