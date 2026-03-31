from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.index,           name='index'),

    # Auth
    path('api/login/',          views.api_login,       name='api_login'),
    path('api/logout/',         views.api_logout,      name='api_logout'),
    path('api/me/',             views.api_me,          name='api_me'),

    # Books
    path('api/books/',          views.api_books,       name='api_books'),
    path('api/books/<int:id>/', views.api_book_detail, name='api_book_detail'),
]