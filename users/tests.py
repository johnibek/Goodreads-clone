from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

from users.models import CustomUser

class RegisterUserTestCase(TestCase):
    def test_user_creation(self):
        self.client.post(
            reverse('users:register'),
            data={
                "username": "mike",
                "first_name": "Mike",
                "last_name": "Watson",
                "email": "mike@mail.com",
                "password1": "somepassword",
                "password2": 'somepassword',
            }
        )

        user = CustomUser.objects.get(username='mike')
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertEqual(user.first_name, "Mike")
        self.assertEqual(user.last_name, "Watson")
        self.assertEqual(user.email, "mike@mail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                'first_name': 'Mike',
                'email': 'mike@mail.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)

        # For django==5.0.4
        form = response.context['form']
        self.assertFormError(form, 'username', 'This field is required.')

        # For django==4.0
        # self.assertFormError(response, 'form', 'username', 'This field is required.')
        # self.assertFormError(response, 'form', 'password1', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'mike',
                'first_name': 'Mike',
                'last_name': 'Thomas',
                'email': 'invalid-email',
                'password': 'mike123'
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)

        form = response.context['form']
        self.assertFormError(form, 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        # 1. create a user
        user1 = CustomUser.objects.create(
            username='john',
            first_name='John'
        )
        user1.set_password('john123')
        user1.save()

        # 2. try to create another user with the same username
        user2 = self.client.post(
            reverse('users:register'),
            data={
                'username': 'john',
                'first_name': 'Jonathan',
                'last_name': 'Taylor',
                'email': 'john@mail.com',
                'password': 'john123'
            }
        )

        # 3. check that the second user was not created
        users_count = CustomUser.objects.count()

        self.assertEqual(users_count, 1)

        # 4. check that the form contains the error message
        form = user2.context['form']
        self.assertFormError(form, 'username', 'A user with that username already exists.')

        # self.assertFormError(user2, 'form', 'username', 'A user with that username already exists.')

class LoginUserTestCase(TestCase):
    def setUp(self):
        db_user = CustomUser(
            username='john',
            first_name='John',
            last_name='Watson'
        )
        db_user.set_password('john123')
        db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'john',
                'password': 'john123'
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        # Test for wrong username
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong_username',
                'password': 'john123'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        # Test for wrong password
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'john',
                'password': 'wrong_password'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='john', password='john123')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser(
            username='john',
            first_name='John',
            last_name='Watson',
            email='john@mail.com'
        )
        user.set_password('john123')
        user.save()

        self.client.login(username='john', password='john123')

        response = self.client.get(reverse('users:profile'))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        user = CustomUser(username='john', first_name='John')
        user.set_password('john123')
        user.save()

        self.client.login(username='john', password='john123')

        response = self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'john',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@mail.com'
            }
        )

        updated_user = CustomUser.objects.get(pk=user.pk)

        # It is the second way of updating user data in db
        # user.refresh_from_db()

        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.email, 'john@mail.com')
        self.assertEqual(response.url, reverse('users:profile'))
        self.assertEqual(response.status_code, 302)

