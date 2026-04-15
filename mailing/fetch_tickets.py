from datetime import time
from email import policy
from email.parser import BytesParser
import imaplib
import os
from email.parser import Parser
import email.utils
from customers.models import Customer

# How often to fetch new tickets, in seconds
FREQ = 30

def request_mail():
    server_host = os.getenv("MAIL_HOST")
    server_port = int(os.getenv("MAIL_PORT", "993"))
    mail_addr = os.getenv("EMAIL")
    mail_pass = os.getenv("PASS")

    print(repr(os.getenv("MAIL_HOST")))
    
    # Login with credentials
    inbox = imaplib.IMAP4_SSL(server_host, server_port)
    inbox.login(mail_addr, mail_pass)
    print("Logged in successfully")

    # Check the status of the inbox, exit if not OK
    status, data = inbox.select('"cpsc"')
    print(f"Select status: {status}, data: {data}")
    if status != "OK":
        print("Could not find specified inbox.")
        inbox.logout()
        return []

    status, data = inbox.search(None, "UNSEEN")
    print(f"Search status: {status}, email IDs found: {data}")
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


import time

def start_email_fetcher():
    from tickets.models import Ticket

    print(f"Fetching tickets every {FREQ} seconds")

    while True:
        try:
            emails = request_mail()
        
            for msg in emails:

                # Get subject/body/from of the email
                subject = msg.get("Subject", "No Subject")
                body_part = msg.get_body(preferencelist=('plain',))
                from_header = msg.get("From", "Unknown <unknown@example.com>")

                if body_part:
                    body = body_part.get_content()
                else:
                    body = "No text content found."
                    
                
                # Parse the sender email
                raw_name, email_address = email.utils.parseaddr(from_header)
                if not email_address:
                    email_address = "unknown@example.com"
                    
                # We have to turn the sender into a customer object 
                raw_name = raw_name.strip() or "Unknown"

                # At most 2 parts, since they could have middle name too
                name_parts = raw_name.split(" ", 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else "User"

                customer, created = Customer.objects.get_or_create(
                    email=email_address[:30],
                    defaults={
                        "first_name": first_name[:30],
                        "last_name": last_name[:30],
                    }
                )
     
                # Making a new ticket will fire off the signal in tickets/signals
                Ticket.objects.create(
                    subject=subject[:50], 
                    message_body=body,
                    customer_email=customer
                )

        except Exception as e:
            print("An error occurred while fetching emails:", e)

        time.sleep(FREQ)
