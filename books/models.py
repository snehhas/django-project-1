from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    copies_available = models.IntegerField(default=5)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    # Add more fields as needed

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.borrowed_date:
            self.borrowed_date = datetime.now()
        if not self.returned_date:
            self.returned_date = self.borrowed_date + timedelta(weeks=1)
        super(BorrowedBook, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
    @property
    def is_overdue(self):
        if self.returned_date:
            return self.returned_date > self.borrowed_date + timezone.timedelta(days=7)
        else:
            return timezone.now() > self.borrowed_date + timezone.timedelta(days=7)

    @property
    def calculate_fine(self):
        if self.is_overdue:
            # Calculate fine amount (e.g., Rs. 5 per day)
            overdue_days = (timezone.now() - (self.borrowed_date + timezone.timedelta(days=7))).days
            fine_amount = overdue_days * 5  # Rs. 5 per day
            if fine_amount > 0:
                return fine_amount
            else:
                return 0
        else:
            return 0  # No fine if not overdue
        
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255, default='') 
    reserved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def save(self, *args, **kwargs):
        self.book_title = self.book.title  # Set the book title
        super().save(*args, **kwargs)
        self.book.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.book.save()

    def __str__(self):
        return f"{self.user.username} reserved {self.book.title}"
