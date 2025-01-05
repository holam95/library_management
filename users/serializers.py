from rest_framework import serializers
from .models import LibraryUser

class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'