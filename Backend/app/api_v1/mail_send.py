import smtplib
from .mail_config import conf

sender = "from@example.com"
receiver = "to@example.com" 

def sendmessage(
    username: str,
    order_id: int,
    total: int
):
      

    subject = "Your Order Confirmation"
    body = f"Hello!\n\nYour order #{order_id} has been successfully created.\nTotal price: {total}."

    message = f"""\
    From: {sender}
    To: {receiver}
    Subject: {subject}

    {body}
    """

    with smtplib.SMTP("smtp.mailmug.net", 2525) as server:
        server.login("9ujuxusw3sw73dqn", "dbsysahqtlk4jkgm")
        server.sendmail(sender, receiver, message)



def send_forgot_password(
        username: str,
        user_email: str,
        token:str
):
    # sender = "shop@mail.com"
    # receiver = f"{user_email}"
    sender = "shop@mail.com"
    receiver = "you@mailmug.net"
    subject = "Password Reset"
    body = f"""Hello!

{user_email} ,
We received a request to reset your password.
Use the token below in the API /reset_password route:

{token}

This token is valid for 5 minutes.

If you did not request this, simply ignore this message."""

    message = f"""\
From: {sender}
To: {receiver}
Subject: {subject}

{body}
"""

    with smtplib.SMTP("smtp.mailmug.net", 2525) as server:
        server.login("9ujuxusw3sw73dqn", "dbsysahqtlk4jkgm")
        server.sendmail(sender, receiver, message)