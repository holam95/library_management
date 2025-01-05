from django.db import models

# Create your models here.
from django.db import models
from books.models import Book
from users.models import LibraryUser

class Transaction(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {'Returned' if self.return_date else 'Borrowed'}"