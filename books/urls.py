from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_add, name='book_add'),
    path('<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    # Add more URLs as needed
]
