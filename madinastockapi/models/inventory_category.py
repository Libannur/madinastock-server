from django.db import models


class InventoryCategory(models.Model):
    """Junction table for many-to-many relationship between Inventory and Category"""
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('inventory', 'category')
        verbose_name = "Inventory Category"
        verbose_name_plural = "Inventory Categories"

    def __str__(self):
        return f"{self.inventory.name} - {self.category.name}"
