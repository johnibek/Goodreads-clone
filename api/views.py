from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import viewsets

from books.models import BookReview
from .serializers import BookReviewSerializer


class BookReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BookReview.objects.all().order_by('created_at')
    serializer_class = BookReviewSerializer
    lookup_field = 'id'
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        super().perform_create(serializer)

# class BookReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all()
#     lookup_field = 'id'
#
#     # def get(self, request, id):
#     #     try:
#     #         book_review = BookReview.objects.get(id=id)
#     #     except BookReview.DoesNotExist:
#     #         return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
#     #
#     #     serializer = BookReviewSerializer(book_review, many=False)
#     #     return Response(serializer.data)
#     #
#     # def delete(self, request, id):
#     #     try:
#     #         book_review = BookReview.objects.get(id=id)
#     #     except BookReview.DoesNotExist:
#     #         return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
#     #
#     #     book_review.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
#     #
#     # def put(self, request, id):
#     #     try:
#     #         book_review = BookReview.objects.get(id=id)
#     #     except BookReview.DoesNotExist:
#     #         return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
#     #
#     #     serializer = BookReviewSerializer(instance=book_review, data=request.data)
#     #
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_200_OK)
#     #
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     #
#     # def patch(self, request, id):
#     #     try:
#     #         book_review = BookReview.objects.get(id=id)
#     #     except BookReview.DoesNotExist:
#     #         return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
#     #
#     #     serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)
#     #
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_200_OK)
#     #
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class BookReviewListAPIView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all().order_by('created_at')
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     # def get(self, request):
#     #     book_reviews = BookReview.objects.all().order_by('created_at')
#     #     paginator = PageNumberPagination()
#     #     page_obj = paginator.paginate_queryset(book_reviews, request)
#     #     serializer = BookReviewSerializer(page_obj, many=True)
#     #     return paginator.get_paginated_response(serializer.data)
#     #
#     # def post(self, request):
#     #     serializer = BookReviewSerializer(data=request.data)
#     #
#     #     if serializer.is_valid():
#     #         serializer.save(user=request.user)
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

