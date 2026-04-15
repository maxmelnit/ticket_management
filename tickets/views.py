from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tickets.models import TicketAssignment

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