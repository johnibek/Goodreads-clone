from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'api'
router = DefaultRouter()
router.register('reviews', views.BookReviewsViewSet, basename='review')

urlpatterns = router.urls

# urlpatterns = [
#     path('reviews/<int:id>', views.BookReviewDetailAPIView.as_view(), name='review-detail'),
#     path('reviews/', views.BookReviewListAPIView.as_view(), name='review-list'),
# ]
