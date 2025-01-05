from django.shortcuts import render # type: ignore

# Create your views here.
from rest_framework import viewsets, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import action # type: ignore
from django.utils.timezone import now # type: ignore
from .models import Transaction
from .serializers import TransactionSerializer
from books.models import Book # type: ignore

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['get'])
    def user_history(self, request):
        """View borrowing history of the authenticated user."""
        transactions = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Check out a book."""
        book_id = request.data.get('book')
        book = Book.objects.get(id=book_id)

        if book.copies_available < 1:
            return Response({"error": "No available copies."}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()

        serializer = self.get_serializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Return a checked-out book."""
        transaction = self.get_object()

        if transaction.return_date is not None:
            return Response({"error": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)

        transaction.return_date = now()
        transaction.save()

        transaction.book.copies_available += 1
        transaction.book.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)