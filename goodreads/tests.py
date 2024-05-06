from django.test import TestCase
from books.models import Book, BookReview
from django.urls import reverse

from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='title1', description='description1', isbn='12345678')

        user = CustomUser(username='john')
        user.set_password('somepassword')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="nice book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="very good book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="not bad")


        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
        self.assertNotContains(response, review1.comment)
