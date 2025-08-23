from django.db import models


class Category(models.Model):
    # Firebase UID (changed from uid for consistency)
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
