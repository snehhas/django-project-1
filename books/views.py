from django.shortcuts import render, redirect, get_object_or_404
from .models import BookForm, Book, BorrowedBook
from django.contrib.auth.decorators import login_required

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

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

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # Create a BorrowedBook record
    borrowed_book = BorrowedBook.objects.create(user=request.user, book=book)
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