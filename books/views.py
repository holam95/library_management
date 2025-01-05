from rest_framework import viewsets, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import action # type: ignore
from .models import Book, Checkout
from .serializers import BookSerializer, CheckoutSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly # type: ignore

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def available_books(self, request):
        """View all books and filter by availability."""
        queryset = self.queryset.filter(copies_available__gt=0)

        # Search filters
        title = request.query_params.get('title', None)
        author = request.query_params.get('author', None)
        isbn = request.query_params.get('isbn', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if isbn:
            queryset = queryset.filter(isbn__icontains=isbn)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Return a checked-out book."""
        checkout = self.get_object()
        if checkout.return_date is not None:
            return Response({"error": "Book is already returned."}, status=status.HTTP_400_BAD_REQUEST)

        # Update book copies
        checkout.book.copies_available += 1
        checkout.book.save()

        # Set the return date
        checkout.return_date = timezone.now()
        checkout.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)