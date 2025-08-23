from django.db import models
from .suppliers import Supplier
from .categories import Category


class Inventory(models.Model):
    UNIT_CHOICES = [
        ('lbs', 'Pounds'),
        ('oz', 'Ounces'),
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('gallons', 'Gallons'),
        ('liters', 'Liters'),
        ('pieces', 'Pieces'),
        ('dozen', 'Dozen'),
        ('cases', 'Cases'),
        ('bottles', 'Bottles'),
        ('cans', 'Cans'),
    ]

    user_id = models.CharField(max_length=255)  # Firebase UID
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name='inventory_items')
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    notes = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # Many-to-many relationship with categories
    categories = models.ManyToManyField(
        Category, through='InventoryCategory', related_name='inventory_items')

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.supplier.name}"
