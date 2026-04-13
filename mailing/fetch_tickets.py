from datetime import time
from email import policy
from email.parser import BytesParser
import imaplib
import os
from email.parser import Parser

# How often to fetch new tickets, in seconds
FREQ = 30

def request_mail():
    server_host = os.getenv("MAIL_HOST")
    server_port = int(os.getenv("MAIL_PORT", "993"))
    mail_addr = os.getenv("EMAIL")
    mail_pass = os.getenv("PASS")

    # Login with credentials
    inbox = imaplib.IMAP4_SSL(server_host, server_port)
    inbox.login(mail_addr, mail_pass)
    inbox.select("INBOX")

    # Check the status of the inbox, exit if not OK
    status, data = inbox.search(None)
    if status != "OK":
        inbox.logout()
        return []

    # The list of messages we'll fetch
    messages = []

    # Go through each email and get the contents of each (raw contents and everything)
    for email_id in data[0].split():
        status, msg_data = inbox.fetch(email_id, "(RFC822)")
        
        # In case of faliure, just move on to the next
        if status != "OK":
            continue

        # Convert from raw bytes to email object, then append to messages
        raw_email = msg_data[0][1]
        msg = BytesParser(policy=policy.default).parsebytes(raw_email)
        messages.append(msg)

    inbox.logout()
    return messages


if __name__ == "__main__":
    while True:
        emails = request_mail()
        for msg in emails:
            print("Subject:", msg.get("Subject"))
            print("From:", msg.get("From"))
            print()

        time.sleep(FREQ)


