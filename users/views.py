from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import LibraryUser
from .serializers import LibraryUserSerializer

class LibraryUserViewSet(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer