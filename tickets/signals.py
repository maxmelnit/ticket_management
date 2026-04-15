import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Ticket, TicketAssignment
from ticket_routing.router import route, find_employee

logger = logging.getLogger(__name__)


# Every time we make a ticket, we need a ticket assignment to some employee that can handle it
@receiver(post_save, sender=Ticket)
def create_ticket_assignment(instance, created, **kwargs):
    priority = None
    clearance = None
    language_code = None
    
    if created:

        # Find an employee that is able to take the ticket
        try:
            employee = find_employee(priority, clearance, language_code)
        except Exception as e:
            logger.log("No suitable support employee available for ticket.")

        TicketAssignment.objects.create(
            ticket=instance,
            clearance_required=clearance,
            priority=priority,
            employee_assigned_to=employee,
        )
