from rest_framework import serializers
from books.models import BookReview, Book
from users.models import CustomUser

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class BookReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ('id', 'comment', 'stars_given', 'book', 'user', 'book_id')
