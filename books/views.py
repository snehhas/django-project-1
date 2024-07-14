from django.shortcuts import render, redirect, get_object_or_404
from .models import BookForm, Book, BorrowedBook, Reservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'query': query})

@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
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

    if request.method == 'POST':
        if book.copies_available > 0:
            BorrowedBook.objects.create(user=request.user, book=book)
            book.copies_available -= 1
            book.save()
        else:
            pass

    return redirect('book_list')

@login_required
def borrowed_books_list(request):
    borrowed_books = BorrowedBook.objects.all()
    return render(request, 'books/borrowed_books_list.html', {'borrowed_books': borrowed_books})

@login_required
def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, pk=borrowed_book_id)
    book = borrowed_book.book
    
    if request.method == 'POST':
        borrowed_book.returned_date = timezone.now()
        borrowed_book.save()

        book.copies_available += 1
        book.save()

        borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
        borrowed_book.delete()
    
    return redirect('borrowed_books_list')

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    existing_reservation = Reservation.objects.filter(user=request.user, book=book).exists()

    if existing_reservation:
        return redirect('book_list')

    reservation = Reservation(user=request.user, book=book)
    reservation.book_title = book.title
    reservation.save()

    # book.is_reserved = True
    # book.save()

    return redirect('book_list')

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    reservation.delete()
    messages.success(request, 'Reservation has been cancelled.')
    return redirect('reserve_view')

@login_required
def reserve_view(request):
    reservations = Reservation.objects.all()
    return render(request, 'books/reserve.html', {'reservations': reservations})

@login_required
def loan_book(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        book = get_object_or_404(Book, pk=reservation.book_id)
        
        try:
            book = reservation.book
            
            borrowed_book = BorrowedBook(user=request.user, book=book)
            borrowed_book.save()
            
            reservation.delete()

            book.is_reserved = False
            book.save()
            
            if book.copies_available > 0:
                book.copies_available -= 1
                book.save()

            return redirect('borrowed_books_list')
        
        except Exception as e:
            messages.error(request, f'Error loaning the book: {e}')
            return redirect('reserve_view')
    
    return redirect('reserve_view')