import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Ticket, TicketAssignment
from ticket_routing.router import route, find_employee

logger = logging.getLogger(__name__)


# Every time we make a ticket, we need a ticket assignment to some employee that can handle it
@receiver(post_save, sender=Ticket)
def create_ticket_assignment(sender, instance, created, **kwargs):
    if created:
        # Defaults in case the AI router is unavailable
        priority = "medium"
        clearance = 1
        language_code = "en"
        employee = None

        try:
            # Use the AI router to determine priority, tier, and language
            result = route(instance)
            priority = result.get("priority", "medium")
            clearance = result.get("tier", 1)
            language_code = result.get("language", "en")

            # Find an employee that is able to take the ticket
            employee = find_employee(priority, clearance, language_code)
        except Exception as e:
            logger.warning(f"Ticket routing failed for Ticket #{instance.id}: {e}")

        TicketAssignment.objects.create(
            ticket=instance,
            clearance_required=clearance,
            priority=priority,
            employee_assigned_to=employee,
        )
