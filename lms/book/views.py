from django.http import QueryDict
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, filters,viewsets,status
from .serializers import (
    BookSerializer, BookCreateUpdateSerializer,
    AuthorSerializer, BorrowRequestSerializer, GenreSerializer,
    BookReviewSerializer,RegisterSerializer
) 
from .models import User,Book, Author, Genre, BorrowRequest, BookReview
from .permissions import IsLibrarian, IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related("author").prefetch_related("genres")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author__name", "genres__name"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "author__name"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BookCreateUpdateSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsLibrarian()]
        return [permissions.AllowAny()]
    

    @action(detail=True, methods=["get"], url_path="allreview", permission_classes=[IsOwnerOrReadOnly])
    def list_reviews(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        reviews = BookReview.objects.filter(book=book).select_related("user")
        serializer = BookReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="reviews", permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        print(pk,"lllllll")
        book = get_object_or_404(Book, pk=pk)
        if BookReview.objects.filter(user=request.user, book=book).exists():
            return Response(
                {"error": "You have already reviewed this book."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if isinstance(request.data,QueryDict):
            request.data._mutable = True
            request.data['book']=pk

        serializer = BookReviewSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorViewSet(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLibrarian()]
        return [permissions.AllowAny()]


class GenreViewSet(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLibrarian()]
        return [permissions.AllowAny()]
    



class BorrowRequestViewSet(viewsets.ModelViewSet):
    queryset = BorrowRequest.objects.select_related("book", "user")
    serializer_class = BorrowRequestSerializer 

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)
        if book.available_copies <= 0:
            return Response({"error": "Book not available"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.role != "STUDENT":
            return Response({"error": "Dont have permission"}, status=status.HTTP_400_BAD_REQUEST)

        borrow = BorrowRequest.objects.create(book=book, user=request.user)
        return Response({"message": "Borrow request created."}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if user.role == "LIBRARIAN":
            return BorrowRequest.objects.all()
        return BorrowRequest.objects.filter(user=user)

    @action(detail=True, methods=["patch"], permission_classes=[IsLibrarian])
    def approve(self, request, pk=None):
        borrow = self.get_object()
        borrow.status = BorrowRequest.StatusChoices.APPROVED
        borrow.approved_at = timezone.now()
        borrow.save()
        return Response({"status": "approved"})

    @action(detail=True, methods=["patch"], permission_classes=[IsLibrarian])
    def reject(self, request, pk=None):
        borrow = self.get_object()
        borrow.status = BorrowRequest.StatusChoices.REJECTED
        borrow.save()
        return Response({"status": "rejected"})

    @action(detail=True, methods=["patch"],url_path="return")
    def return_book(self, request, pk=None):
        borrow = self.get_object()
        borrow.status = BorrowRequest.StatusChoices.RETURNED
        borrow.returned_at = timezone.now()
        borrow.save()
        return Response({"status": "returned"})