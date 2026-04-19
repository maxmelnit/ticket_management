from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from tickets.models import TicketAssignment
from django.contrib.auth import logout

def login_view(request):

    # Authenticate users on login form submission:
    if request.method == "POST":

        employee_id = request.POST.get("employee_id")
        password = request.POST.get("password")
        user = authenticate(request, employee_id=employee_id, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Employee ID or password is incorrect.")

    # Render login page regardless (GET)
    return render(request, "login.html")

@login_required
def dashboard_view(request):
    # Get the dashboard view for employees
    
    assignments = TicketAssignment.objects.filter(employee_assigned_to=request.user)

    context = {
        "open_count": assignments.filter(ticket__status="open").count(),
        "pending_count": assignments.filter(ticket__status="pending").count(),
        "closed_count": assignments.filter(ticket__status="closed").count(),
    }

    return render(request, "dashboard.html", context)

def logout_view(request):
    logout(request)
    return redirect("login")