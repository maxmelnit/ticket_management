from django.contrib import admin
from .models import Language, TicketRouter, IssueType, Ticket, TicketAssignment, TicketEscalation, EmployeeLanguage

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("language_code", "language_name")

@admin.register(IssueType)
class IssueTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "status", "created_at")
    list_filter = ("status", "issue_type")

@admin.register(TicketAssignment)
class TicketAssignmentAdmin(admin.ModelAdmin):
    list_display = ("assignment_number", "ticket", "employee_assigned_to", "priority", "clearance_required")
    list_filter = ("priority", "clearance_required")

@admin.register(TicketEscalation)
class TicketEscalationAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "employee_id_from", "employee_id_to", "time_created")

@admin.register(EmployeeLanguage)
class EmployeeLanguageAdmin(admin.ModelAdmin):
    list_display = ("employee", "language_code")
