from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):

    # Authenticate users on login form submission:
    if request.method == "POST":

        # Get the employee ID and pass from form
        employee_id = request.POST.get("employee_id")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, employee_id=employee_id, password=password)

        # If that user exists and is correct, send them to the dashboard, otherwise error
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Employee ID or password is incorrect.")

    # Render login page regardless (GET)
    return render(request, "login.html")