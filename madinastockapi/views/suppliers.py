from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models.suppliers import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'user_id', 'name', 'email', 'phone', 'address',
                  'city', 'state', 'zip_code', 'is_active', 'created_date']


class SupplierView(ViewSet):

    def retrieve(self, request, pk):
        """
        Retrieve a single supplier by primary key (ID)
        GET /api/suppliers/{id}/
        """
        try:
            supplier = Supplier.objects.get(pk=pk)
            serializer = SupplierSerializer(supplier)
            return Response(serializer.data)
        except Supplier.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        List all suppliers
        GET /api/suppliers/
        """
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new supplier
        POST /api/suppliers/
        """
        supplier = Supplier.objects.create(
            user_id=request.data["user_id"],
            name=request.data["name"],
            email=request.data["email"],
            phone=request.data["phone"],
            address=request.data["address"],
            city=request.data["city"],
            state=request.data["state"],
            zip_code=request.data["zip_code"],
        )
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """
        Update an existing supplier
        PUT /api/suppliers/{id}/
        """
        supplier = Supplier.objects.get(pk=pk)
        supplier.user_id = request.data["user_id"]
        supplier.name = request.data["name"]
        supplier.email = request.data["email"]
        supplier.phone = request.data["phone"]
        supplier.address = request.data["address"]
        supplier.city = request.data["city"]
        supplier.state = request.data["state"]
        supplier.zip_code = request.data["zip_code"]
        supplier.save()

        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """
        Delete a supplier
        DELETE /api/suppliers/{id}/
        """
        supplier = Supplier.objects.get(pk=pk)
        supplier.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
