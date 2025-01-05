from rest_framework import serializers # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore
from .models import Book, Checkout

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        if Book.objects.filter(isbn=value).exists():
            raise ValidationError("A book with this ISBN already exists.")
        return value

    def validate(self, data):
        if data['copies_available'] < 0:
            raise serializers.ValidationError("Number of available copies cannot be negative.")
        return data


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'

    def validate(self, data):
        # Check if the book has available copies
        if data['book'].copies_available < 1:
            raise serializers.ValidationError(f"No available copies for '{data['book'].title}'.")

        # Check if the user has already checked out the book
        if Checkout.objects.filter(user=data['user'], book=data['book'], return_date__isnull=True).exists():
            raise serializers.ValidationError(f"User '{data['user'].username}' has already checked out this book.")
        
        return data