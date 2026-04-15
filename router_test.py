import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticket_management.settings")
django.setup()

from tickets.models import Ticket
from ticket_routing.router import route, find_employee


def main():
    ticket = Ticket.objects.create(
        subject="Server is down",
        message_body="Our production server is unreachable and customers cannot log in."
    )

    result = route(ticket)
    print("LLM result:", result)

    employee = find_employee(
        result["priority"],
        result["tier"],
        result["language"]
    )

    print("Assigned employee:", employee)


if __name__ == "__main__":
    main()