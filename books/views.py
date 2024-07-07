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
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

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

@login_required
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

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # Check if the user has already reserved this book
    existing_reservation = Reservation.objects.filter(user=request.user, book=book).exists()

    if existing_reservation:
        # Handle case where user has already reserved the book
        # You may want to redirect with a message indicating that the book is already reserved
        return redirect('book_list')

    # Create a new reservation
    reservation = Reservation(user=request.user, book=book)
    reservation.save()

    # Update the book's is_reserved field
    book.is_reserved = True
    book.save()

    return redirect('book_list')

@login_required
def reserve_view(request):
    reservations = Reservation.objects.all()
    return render(request, 'books/reserve.html', {'reservations': reservations})

@login_required
def loan_book(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        
        # Perform actions to loan the book
        try:
            book = reservation.book
            
            # Create a record in borrowed books
            borrowed_book = BorrowedBook(user=request.user, book=book)
            borrowed_book.save()
            
            # Remove the reservation
            reservation.delete()
            
            # Update book availability (if needed)
            book.copies_available -= 1
            book.save()
            
            messages.success(request, f'You have successfully loaned {book.title}.')
            return redirect('borrowed_books_list')
        
        except Exception as e:
            messages.error(request, f'Error loaning the book: {e}')
            return redirect('reserve_view')
    
    # Handle other HTTP methods or invalid scenarios
    return redirect('reserve_view')