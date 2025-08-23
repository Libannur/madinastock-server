from django.db import models


class Supplier(models.Model):
    user_id = models.CharField(max_length=255)  # Firebase UID
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['name']

    def __str__(self):
        return self.name
