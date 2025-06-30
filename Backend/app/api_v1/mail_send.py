import smtplib

sender = "from@example.com"
receiver = "to@example.com" 

def sendmessage(
    username: str,
    order_id: int,
    total: int
):
    sender = "shop@mail.com"
    receiver = "you@mailmug.net"  

    subject = "Your Order Confirmation"
    body = f"Hello, {username}!\n\nYour order #{order_id} has been successfully created.\nTotal price: {total}."

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
        user_id: int,
        user_email: str,
        token:str
):
    sender = "shop@mail.com"
    receiver = f"{user_email}"

    subject = "Password Reset"
    body = f"""Hello, {username}!

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
        server.login("n12bdambb2iwtsba", "6l8dlqhkcgfigg6u")
        server.sendmail(sender, receiver, message)