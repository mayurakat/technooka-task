from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowRequest, Book

@receiver(post_save, sender=BorrowRequest)
def update_book_stock(sender, instance, **kwargs):
    book = instance.book
    if instance.status == BorrowRequest.StatusChoices.APPROVED:
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
    elif instance.status == BorrowRequest.StatusChoices.RETURNED:
        book.available_copies += 1
        book.save()