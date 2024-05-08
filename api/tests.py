from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from books.models import BookReview, Book
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='john', first_name='John', last_name='Watson', email='john@mail.com')
        self.user.set_password('somepassword')
        self.user.save()
        self.client.login(username='john', password='somepassword')

    def test_book_review_detail(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        book_review = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='Very good book')

        response = self.client.get(reverse('api:review-detail', kwargs={'id': book_review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], book_review.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very good book")

        self.assertEqual(response.data['book']['id'], book_review.book.id)
        self.assertEqual(response.data['book']['title'], 'book1')
        self.assertEqual(response.data['book']['description'], 'description1')
        self.assertEqual(response.data['book']['isbn'], '12345678')

        self.assertEqual(response.data['user']['id'], book_review.user.id)
        self.assertEqual(response.data['user']['username'], 'john')
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Watson')
        self.assertEqual(response.data['user']['email'], 'john@mail.com')

        # Test for review that is not available
        response = self.client.get(reverse('api:review-detail', kwargs={'id': 2}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'No BookReview matches the given query.')

    def test_delete_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        book_review = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='Very good book')

        response = self.client.delete(reverse('api:review-detail', kwargs={'id': book_review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        book_review = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='Very good book')

        response = self.client.patch(reverse('api:review-detail', kwargs={'id': book_review.id}), data={'stars_given': 4})
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 4)

    def test_put_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        book_review = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='Very good book')

        response = self.client.put(
            reverse('api:review-detail', kwargs={'id': book_review.id}),
            data={
                'stars_given': 4,
                'comment': "Nice book",
                'book_id': book.id
            }
        )
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 4)
        self.assertEqual(book_review.comment, 'Nice book')

    def test_create_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12345678')

        data = {
            'stars_given': 2,
            'comment': 'bad book',
            'book_id': book.id
        }

        response = self.client.post(
            reverse('api:review-list'),
            data=data
        )
        book_review = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(book_review.stars_given, 2)
        self.assertEqual(book_review.comment, 'bad book')


    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='mike', first_name='Mike', last_name='Thomas', email='mike@mail.com')
        user_two.set_password('somepassword')
        user_two.save()

        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        book_review1 = BookReview.objects.create(user=self.user, book=book, stars_given=4, comment='Nice book')
        book_review2 = BookReview.objects.create(user=user_two, book=book, stars_given=5, comment='Excellent book')

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(len(response.data['results']), 2)

        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(response.data['results'][0]['id'], book_review1.id)
        self.assertEqual(response.data['results'][0]['stars_given'], book_review1.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], book_review1.comment)

        self.assertEqual(response.data['results'][1]['id'], book_review2.id)
        self.assertEqual(response.data['results'][1]['stars_given'], book_review2.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], book_review2.comment)


