from django.contrib import admin

from book.models import Author, Book, BookReview, BorrowRequest, User,Genre

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BorrowRequest)
admin.site.register(BookReview)
