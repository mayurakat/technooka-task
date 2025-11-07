from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.



# 1. Custom User Model
class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        LIBRARIAN = "LIBRARIAN", "Librarian"

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    ISBN = models.CharField(max_length=13, unique=True)
    available_copies = models.PositiveIntegerField(default=0)
    total_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    def is_available(self):
        return self.available_copies > 0


class BorrowRequest(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        RETURNED = "RETURNED", "Returned"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrow_requests")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    requested_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(blank=True, null=True)
    returned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} → {self.book.title} ({self.status})"

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.book.title} - {self.rating}/5 by {self.user.username}"
