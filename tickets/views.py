import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tickets.models import TicketAssignment
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from tickets.models import Ticket, TicketResolution, TicketEscalation, TicketAssignment
from ticket_routing.router import find_employee
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import get_connection


@login_required
def ticket_list_view(request):

    # Get all assignments for the logged-in employee
    assignments = TicketAssignment.objects.filter(employee_assigned_to=request.user).select_related('ticket', 'ticket__issue_type', 'ticket__customer_email')
    
    # Filter by status if provided in the URL (e.g., ?status=open)
    status_filter = request.GET.get('status')
    if status_filter in ['open', 'pending', 'closed']:
        assignments = assignments.filter(ticket__status=status_filter)
        
    # We want a list of tickets, but we have assignments. 
    # Let's extract the tickets and attach the assignment priority to them for display.
    tickets = []
    for assignment in assignments:
        ticket = assignment.ticket
        # attach priority and assignment info directly to the ticket object for the template
        ticket.priority = assignment.priority
        ticket.assignment_number = assignment.assignment_number
        tickets.append(ticket)

    context = {
        'tickets': tickets,
        'current_status': status_filter or 'All',
    }
    return render(request, "ticket_list.html", context)


@login_required
def ticket_detail_view(request, ticket_id):

    # Get the actual ticket for the specific ticket id
    ticket = Ticket.objects.get(id=ticket_id)
    
    assignment = TicketAssignment.objects.filter(ticket=ticket).first()
    if assignment:
        ticket.priority = assignment.priority

    # Use post to submit a ticket resolution in the form
    if request.method == "POST":
        resolution_body = request.POST.get("resolution_body", "").strip()

        # Make a new ticket resolution, with the filled details
        TicketResolution.objects.create(
            resolution_subject=f"RE: {ticket.subject}",
            resolution_body=resolution_body,
            ticket=ticket,
            employee=request.user
        )

        # Use SMTP to send the resolution back to the customer (we actually emailing it back)
        if ticket.customer_email and ticket.customer_email.email:
            try:

                connection = get_connection(
                backend="django.core.mail.backends.smtp.EmailBackend",
                host="smtp.gmail.com",
                port=587,
                username=os.getenv("EMAIL"),
                password=os.getenv("PASS"),
                use_tls=True,
                fail_silently=False,
)
                send_mail(
                    subject=f"RE: {ticket.subject}",
                    message=resolution_body,

                    # This is the email I've configured to send the email back to the customer
                    # It's for dbms class so just using one of my personal emails
                    from_email=os.getenv("EMAIL"),
                    recipient_list=[ticket.customer_email.email],
                    connection=connection,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Couldn't send email: {e}")

        # Close the ticket, save it, and redirect back to the dashboard
        ticket.status = "closed"
        ticket.save()
        return redirect("dashboard")

    # In the case that we just open the ticket, we move it to open from pending
    if ticket.status == "pending":
        ticket.status = "open"
        ticket.save()

    return render(request, "ticket_detail.html", {"ticket": ticket})


@login_required
def escalate_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    assignment = TicketAssignment.objects.get(ticket=ticket)

    # We can escalate tickets for employees in tiers 1, 2, 3
    if request.user.tier < 4:
        current_tier = request.user.tier
        next_tier = current_tier + 1

        # Determine the language of ticket and assign it to a new employee
        language_code = "en-US"
        if ticket.lang_code:
            language_code = ticket.lang_code.language_code


        new_employee = find_employee(assignment.priority, next_tier, language_code)

        # Log the escalation
        TicketEscalation.objects.create(
            ticket=ticket,
            employee_id_from=request.user,
            employee_id_to=new_employee,
            escalation_reason=f"Automated escalation from Tier {current_tier} to Tier {next_tier}"
        )

        # Update the assignment
        assignment.clearance_required = next_tier
        assignment.employee_assigned_to = new_employee
        assignment.save()

    return redirect("dashboard")