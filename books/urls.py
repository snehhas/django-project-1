from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_add, name='book_add'),
    path('<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('borrowed_books/', views.borrowed_books_list, name='borrowed_books_list'),
    path('return/<int:borrowed_book_id>/', views.return_book, name='return_book'),
    path('books/reserve/<int:book_id>/', views.reserve_book, name='reserve_book'),
    path('reserve/', views.reserve_view, name='reserve_view'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('loan-book/<int:reservation_id>/', views.loan_book, name='loan_book'),
    path('books/update/<int:pk>/', views.book_update, name='book_update'),
    path('<int:pk>/delete/', views.delete_book, name='delete_book'),
]
