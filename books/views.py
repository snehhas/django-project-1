from django.shortcuts import render, redirect, get_object_or_404
from .models import BookForm, Book, BorrowedBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'query': query})

def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        # Check if there are available copies to borrow
        if book.copies_available > 0:
            # Create a BorrowedBook instance
            BorrowedBook.objects.create(user=request.user, book=book)
            
            # Update copies_available count
            book.copies_available -= 1
            book.save()

            messages.success(request, f'You have borrowed "{book.title}"')
        else:
            messages.error(request, f'Sorry, "{book.title}" is currently not available for loan.')

    return redirect('book_list')

@login_required
def borrowed_books_list(request):
    borrowed_books = BorrowedBook.objects.all()
    return render(request, 'books/borrowed_books_list.html', {'borrowed_books': borrowed_books})

@login_required
def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
    borrowed_book.delete()
    return redirect('borrowed_books_list')

def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, pk=borrowed_book_id)
    book = borrowed_book.book
    
    if request.method == 'POST':
        # Update returned_date for the BorrowedBook instance
        borrowed_book.returned_date = timezone.now()
        borrowed_book.save()

        # Increase copies_available count for the returned book
        book.copies_available += 1
        book.save()

        borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
        borrowed_book.delete()

        messages.success(request, f'You have returned "{book.title}"')
    
    return redirect('borrowed_books_list')