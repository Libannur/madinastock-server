from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models.inventory import Inventory
from ..models.categories import Category


class InventoryInputSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating inventory - accepts IDs"""
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Inventory
        fields = ['id', 'user_id', 'supplier', 'name',
                  'description', 'unit', 'notes', 'price', 'created_date', 'categories']


class InventoryDisplaySerializer(serializers.ModelSerializer):
    """Serializer for displaying inventory - shows names"""
    supplier = serializers.StringRelatedField(read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'user_id', 'supplier', 'name',
                  'description', 'unit', 'notes', 'price', 'created_date', 'categories']


class InventoryView(ViewSet):

    def retrieve(self, request, pk):
        """
        Retrieve a single inventory item by primary key (ID)
        GET /api/inventory/{id}/
        """
        try:
            inventory = Inventory.objects.prefetch_related(
                'categories').get(pk=pk)
            serializer = InventoryDisplaySerializer(inventory)
            return Response(serializer.data)
        except Inventory.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        List all inventory items
        GET /api/inventory/
        """
        inventory_items = Inventory.objects.prefetch_related(
            'categories', 'supplier').all()
        serializer = InventoryDisplaySerializer(inventory_items, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new inventory item
        POST /api/inventory/
        """
        inventory = Inventory.objects.create(
            user_id=request.data["user_id"],
            supplier_id=request.data["supplier"],
            name=request.data["name"],
            description=request.data.get("description", ""),
            unit=request.data["unit"],
            notes=request.data.get("notes", ""),
            price=request.data.get("price", None),
        )
        inventory.categories.set(request.data.get("categories", []))
        serializer = InventoryDisplaySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """
        Update an existing inventory item
        PUT /api/inventory/{id}/
        """
        inventory = Inventory.objects.get(pk=pk)
        inventory.user_id = request.data["user_id"]
        inventory.supplier_id = request.data["supplier"]
        inventory.name = request.data["name"]
        inventory.description = request.data.get("description", "")
        inventory.unit = request.data["unit"]
        inventory.notes = request.data.get("notes", "")
        inventory.price = request.data.get("price", None)
        inventory.save()
        inventory.categories.set(request.data.get("categories", []))
        serializer = InventoryDisplaySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """
        Delete an inventory item
        DELETE /api/inventory/{id}/
        """
        inventory = Inventory.objects.get(pk=pk)
        inventory.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
