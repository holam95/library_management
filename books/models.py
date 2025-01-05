from django.db import models
from users.models import LibraryUser  # Import user model

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Checkout(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, related_name='checkouts')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='checkouts')
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"