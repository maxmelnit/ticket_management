from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from customers.models import Customer


class Language(models.Model):
    language_code = models.CharField(primary_key=True, max_length=8)
    language_name = models.CharField(max_length=30)

    class Meta:
        db_table = "language"

    def __str__(self):
        return f"{self.language_code} - {self.language_name}"


class TicketRouter(models.Model):
    ai_model_id = models.CharField(primary_key=True, max_length=30)
    ai_model_name = models.CharField(max_length=30)

    class Meta:
        db_table = "ticket_router"

    def __str__(self):
        return self.ai_model_name


class IssueType(models.Model):
    issue = models.CharField(primary_key=True, max_length=20)

    class Meta:
        db_table = "issue_type"

    def __str__(self):
        return self.issue


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("pending", "Pending"),
    ]

    subject = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message_body = models.TextField()

    issue_type = models.ForeignKey(
        IssueType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer_email = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    router_model_id = models.ForeignKey(
        TicketRouter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    lang_code = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ticket"

    def __str__(self):
        return f"Ticket #{self.id}: {self.subject}"


class TicketResolution(models.Model):
    resolution_subject = models.CharField(max_length=50)
    resolution_body = models.TextField()
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ticket_resolution"

    def __str__(self):
        return self.resolution_subject


class TicketEscalation(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    escalation_reason = models.CharField(max_length=50)
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    employee_id_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="escalations_sent",
    )
    employee_id_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="escalations_received",
    )

    class Meta:
        db_table = "ticket_escalation"

    def __str__(self):
        return f"Escalation #{self.id}"


class TicketAssignment(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    assignment_number = models.IntegerField(primary_key=True)
    clearance_required = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    assigned_at = models.DateTimeField(auto_now_add=True)
    employee_assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ticket_assignment"

    def __str__(self):
        return f"Assignment #{self.assignment_number}"


class EmployeeLanguage(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    language_code = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "employee_language"
        unique_together = ("employee", "language_code")

    def __str__(self):
        return f"{self.employee} - {self.language_code}"