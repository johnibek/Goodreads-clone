from django.test import TestCase
from django.urls import reverse
from .models import Book, Author, BookAuthor, BookReview
from users.models import CustomUser

class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        # We ordered the book list by "-id"
        book3 = Book.objects.create(title='title1', description='description1', isbn='111111')
        book2 = Book.objects.create(title='title2', description='description2', isbn='222222')
        book1 = Book.objects.create(title='title3', description='description3', isbn='333333')


        response = self.client.get(reverse('books:list') + '?page=1&page_size=2')

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?page=2&page_size=2')
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title='title1', description='description1', isbn='123123')
        author = Author.objects.create(first_name='Walter', last_name='Isaacson', email='walter@mail.com', bio="Author of Steve Jobs")
        book_author = BookAuthor.objects.create(book=book, author=author)

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, author.full_name())

    def test_search_books(self):
        book3 = Book.objects.create(title='Sport', description='description1', isbn='111111')
        book2 = Book.objects.create(title='Guide', description='description2', isbn='222222')
        book1 = Book.objects.create(title='Job', description='description3', isbn='333333')

        response = self.client.get(reverse('books:list') + '?q=sport')

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)

        response = self.client.get(reverse('books:list') + '?q=guide')

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)
        self.assertNotContains(response, book1.title)

        response = self.client.get(reverse('books:list') + '?q=job')

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)


class BookReviewTestCase(TestCase):
    def setUp(self):
        self.book = Book(
            title='Title1',
            description='Description1',
            isbn='12345678'
        )
        self.book.save()

        self.user = CustomUser(
            username='john',
            first_name='John',
            last_name='Watson',
            email='john@mail.com'
        )
        self.user.set_password('somepassword')
        self.user.save()

    def test_add_review(self):
        self.client.login(username='john', password='somepassword')

        self.client.post(
            reverse('books:reviews', kwargs={'id': self.book.id}),
            data={
                'stars_given': 3,
                'comment': 'Nice book'
            }
        )

        book_reviews = self.book.reviews.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].book, self.book)
        self.assertEqual(book_reviews[0].user, self.user)

    # Test wrong inputs
    def test_wrong_comment_inputs(self):
        self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                            data={
                                'stars_given': 3,
                                'comment': 'Not bad'
                            })
        book_reviews = self.book.reviews.all()
        self.assertEqual(book_reviews.count(), 0)

        # Send request as a logged-in user
        self.client.login(username='john', password='somepassword')

        response = self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                         data={
                             'stars_given': 7,
                             'comment': 'Good book'
                                })
        book_reviews = self.book.reviews.all()

        self.assertEqual(book_reviews.count(), 0)
        # Ensure this value is less than or equal to 5.
        form = response.context['form']
        self.assertFormError(form, 'stars_given', 'Ensure this value is less than or equal to 5.')

    # Test required inputs
    def test_required_comment_inputs(self):
        self.client.login(username='john', password='somepassword')

        # Send request without giving stars
        response = self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                         data={
                             'comment': 'Nice Book'
                         })

        book_reviews = self.book.reviews.all()
        form = response.context['form']

        self.assertEqual(book_reviews.count(), 0)
        self.assertFormError(form, 'stars_given', 'This field is required.')

        # Send request without comment
        response = self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                                    data={
                                        'stars_given': 3
                                    })
        form = response.context['form']
        self.assertEqual(book_reviews.count(), 0)
        self.assertFormError(form, 'comment', 'This field is required.')


    def test_edit_review(self):
        self.client.login(username='john', password='somepassword')
        self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                                    data={
                                        'stars_given': 5,
                                        'comment': 'Very good book'
                                    })
        review = BookReview.objects.all()[0]

        self.client.post(reverse('books:edit-review', kwargs={'book_id': self.book.id, 'review_id': review.id}),
                                    data={
                                        'stars_given': 4,
                                        'comment': 'Nice book'
                                    })

        response = self.client.get(reverse('books:detail', kwargs={'id': self.book.id}))

        edited_review = BookReview.objects.all()[0]

        self.assertContains(response, edited_review.stars_given)
        self.assertContains(response, edited_review.comment)
        self.assertNotContains(response, review.comment)
        self.assertNotEqual(review.stars_given, edited_review.stars_given)
        self.assertNotEqual(review.comment, edited_review.comment)

    def test_confirm_delete_review(self):
        self.client.login(username='john', password='somepassword')
        self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                         data={
                             'stars_given': 5,
                             'comment': 'Very good book'
                         })

        review = BookReview.objects.all()[0]

        response = self.client.get(reverse('books:confirm-delete-review', kwargs={'book_id': self.book.id, 'review_id': review.id}))

        self.assertContains(response, self.book.title)
        self.assertContains(response, review.comment)

    def test_delete_review(self):
        self.client.login(username='john', password='somepassword')
        self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                         data={
                             'stars_given': 5,
                             'comment': 'Very good book'
                         })

        review = BookReview.objects.all()[0]

        self.client.get(reverse('books:delete-review', kwargs={'book_id': self.book.id, 'review_id': review.id}))

        review_count = BookReview.objects.count()
        self.assertEqual(review_count, 0)

        response = self.client.get(reverse('books:detail', kwargs={'id': self.book.id}))

        self.assertNotContains(response, review.comment)


class AuthorDetailTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='user', first_name='User')
        self.user.set_password('somepassword')
        self.user.save()
        self.client.login(username='user', password='somepassword')
    def test_author_detail(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        author = Author.objects.create(first_name='John',
                                       last_name='Watson',
                                       email='john@mail.com',
                                       twitter='https://twitter.com/john',
                                       bio='bio1')
        book_author = BookAuthor.objects.create(book=book, author=author)

        response = self.client.get(reverse('books:author-detail', kwargs={'book_id': book.id, 'author_id': author.id}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)
        self.assertContains(response, author.email)
        self.assertContains(response, author.twitter)
        self.assertContains(response, author.bio)


class EditAuthorDetailTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='user', first_name='User')
        self.user.set_password('somepassword')
        self.user.save()
        self.client.login(username='user', password='somepassword')
    def test_edit_author(self):
        self.user.is_superuser = True
        self.user.save()

        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        author = Author.objects.create(first_name='John',
                                       last_name='Watson',
                                       email='john@mail.com',
                                       twitter='https://twitter.com/john',
                                       bio='bio1')

        bookauthor = BookAuthor.objects.create(book=book, author=author)

        self.client.post(
            reverse('books:edit-author-detail', kwargs={'book_id': book.id, 'author_id': author.id}),
            data={
                'first_name': 'John1',
                'last_name': 'Watson1',
                'email': 'john1@mail.com',
                'twitter': 'https://twitter.com/john1',
                'bio': 'bio2'
            }
        )

        author.refresh_from_db()

        self.assertEqual(author.first_name, 'John1')
        self.assertEqual(author.last_name, 'Watson1')
        self.assertEqual(author.email, 'john1@mail.com')
        self.assertEqual(author.twitter, 'https://twitter.com/john1')
        self.assertEqual(author.bio, 'bio2')


        response = self.client.get(
            reverse('books:author-detail', kwargs={'book_id': book.id, 'author_id': author.id})
        )

        self.assertContains(response, 'John1')
        self.assertContains(response, 'Watson1')
        self.assertContains(response, 'john1@mail.com')
        self.assertContains(response, 'https://twitter.com/john1')
        self.assertContains(response, 'bio2')


    def test_author_detail_for_not_admin_user(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12345678')
        author = Author.objects.create(first_name='John',
                                       last_name='Watson',
                                       email='john@mail.com',
                                       twitter='https://twitter.com/john',
                                       bio='bio')

        bookauthor = BookAuthor.objects.create(book=book, author=author)

        response = self.client.post(
            reverse('books:edit-author-detail', kwargs={'book_id': book.id, 'author_id': author.id}),
            data={
                'first_name': 'John1',
                'last_name': 'Watson1',
                'email': 'john1@mail.com',
                'twitter': 'https://twitter.com/john1',
                'bio': 'bio1'
            }
        )

        author.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(author.first_name, 'John1')
        self.assertNotEqual(author.last_name, 'Watson1')
        self.assertNotEqual(author.email, 'john1@mail.com')
        self.assertNotEqual(author.twitter, 'https://twitter.com/john1')
        self.assertNotEqual(author.bio, 'bio1')

        response = self.client.get(
            reverse('books:author-detail', kwargs={'book_id': book.id, 'author_id': author.id})
        )

        self.assertContains(response, 'John')
        self.assertContains(response, 'Watson')
        self.assertContains(response, 'john@mail.com')
        self.assertContains(response, 'https://twitter.com/john')
        self.assertContains(response, 'bio')
