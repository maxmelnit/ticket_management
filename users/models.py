from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class SupportEmployeeManager(BaseUserManager):
    def create_user(self, employee_id, password=None, **extra_fields):
        if not employee_id:
            raise ValueError("The employee_id field is required")

        user = self.model(employee_id=employee_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(employee_id, password, **extra_fields)


class SupportEmployee(AbstractBaseUser, PermissionsMixin):
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    tier = models.IntegerField()

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = SupportEmployeeManager()

    USERNAME_FIELD = "employee_id"
    REQUIRED_FIELDS = ["first_name", "last_name", "tier"]

    def __str__(self):
        return self.employee_id