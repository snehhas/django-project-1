from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_add, name='book_add'),
    path('<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('borrowed_books/', views.borrowed_books_list, name='borrowed_books_list'),
    path('return/<int:borrowed_book_id>/', views.return_book, name='return_book'),
    # Add more URLs as needed
]
