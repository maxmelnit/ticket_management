from django.db import models


class Customer(models.Model):
    email = models.EmailField(primary_key=True, max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)

    class Meta:
        db_table = "customer"

    def __str__(self):
        return self.email