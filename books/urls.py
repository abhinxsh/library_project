from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # API endpoints
    path('api/books/', views.api_books, name='api_books'),
    path('api/books/<int:id>/', views.api_book_detail, name='api_book_detail'),
]