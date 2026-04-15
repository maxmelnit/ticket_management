import json
import ollama  # I'll use an Ollama model to avoid using external APIs, but any LLM provider works


def route(ticket):

    # Want the model to respond back with a JSON schema with info on who to give the ticket to
    schema = {
        "type": "object",
        "properties": {
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"]
            },
            "tier": {
                "type": "integer",
                "enum": [1, 2, 3, 4]
            },
            "language": {"type": "string"}
        },
        "required": ["priority", "tier", "language"]
    }

    # The actual prompt that the model needs to determine priority
    prompt = (
    "Analyze the following support ticket.\n"
    "Use these tier rules:\n"
    "Tier 1: simple account help, password reset, basic questions.\n"
    "Tier 2: billing issues, simple bugs.\n"
    "Tier 3: technical problems that needs deeper investigation, integrations, strong failures.\n"
    "Tier 4: outage, security issues, data loss, system down.\n\n"
    "Use these priority rules:\n"
    "low: It can wait until more important issues are resolved. Simple issues that don't need to be addressed immediately\n"
    "medium: Should be addressed in a timely manner. Think 2-3 business days."
    "high: Should be addressed very quickly. Important issues that have real consequences if not addressed."
    "urgent: Has to be fixed right now. Could cause serious damage if not addressed."
    "Each tier as has the permissions for tiers below it too.\n\n"
    "Return priority, tier, and language.\n"
    "Note that language should use ISO 639-1. For example, en-US, ar-DZ, nl-BE, etc. (Note the region capitalization)"
    "Subject: " + ticket.subject + "\n"
    "Message: " + ticket.message_body + "\n"
    )

    response = ollama.chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': prompt}],
        format=schema,
    )

    print("RAW RESPONSE:", response.message.content)

    result = json.loads(response.message.content)

    return result


# Finds what employee could handle the ticket best. Takes into account the priority, tier, and language of the ticket.
def find_employee(priority, tier, language_code):
    from django.db.models import Count, Q
    from users.models import SupportEmployee

    # Get all the employees within the specified tier
    possible_emps = SupportEmployee.objects.filter(
        tier__gte=tier,
        is_active=True,
        employeelanguage__language_code__language_code=language_code,
    ).annotate(

        # Count the number of tickets an employee alr has
        open_assignments=Count(
            'ticketassignment',
            filter=Q(ticketassignment__ticket__status='open')
        )
        # Give the person with least tickets an assignment first
    ).order_by('open_assignments', 'tier')

    return possible_emps.first() 

# Just test to see if response works
if __name__ == "__main__":
    import os, sys
    import django
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticket_management.settings")
    django.setup()

    from tickets.models import Ticket
    ticket = Ticket(subject="Credit card hacked", message_body="I want my money back or ill charge back")
    result = route(ticket)
    print("Result:", result)