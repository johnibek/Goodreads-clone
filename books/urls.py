from django.urls import path
from . import views


app_name = 'books'
urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<int:id>', views.BookDetailView.as_view(), name='detail'),
    path('<int:id>/reviews/', views.AddReviewView.as_view(), name='reviews'),
    path('<int:book_id>/reviews/<int:review_id>/edit', views.EditReviewView.as_view(), name='edit-review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/confirm', views.ConfirmDeleteReviewView.as_view(), name='confirm-delete-review'),
    path('<int:book_id>/reviews/<int:review_id>/delete', views.DeleteReviewView.as_view(), name='delete-review'),
    path('<int:book_id>/authors/<int:author_id>', views.AuthorDetailView.as_view(), name='author-detail'),
]
