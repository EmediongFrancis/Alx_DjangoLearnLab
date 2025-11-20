from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book model instances to JSON format and vice versa.
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Includes all fields: id, title, author

