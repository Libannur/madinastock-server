from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models.categories import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user_id', 'name', 'description', 'created_date']


class CategoryView(ViewSet):

    def retrieve(self, request, pk):
        """
        Retrieve a single category by primary key (ID)
        GET /api/categories/{id}/
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        List all categories
        GET /api/categories/
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new category
        POST /api/categories/
        """
        category = Category.objects.create(
            user_id=request.data["user_id"],
            name=request.data["name"],
            description=request.data.get("description", "")
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """
        Update an existing category
        PUT /api/categories/{id}/
        """
        category = Category.objects.get(pk=pk)
        category.user_id = request.data["user_id"]
        category.name = request.data["name"]
        category.description = request.data.get("description", "")
        category.save()
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """
        Delete a category
        DELETE /api/categories/{id}/
        """
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
