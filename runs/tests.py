from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Run


class RunLogTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPassword123!'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='TestPassword123!'
        )

        self.run = Run.objects.create(
            user=self.user,
            date=date.today(),
            distance=5.00,
            distance_unit='km',
            duration=timedelta(minutes=30),
            run_type='Easy',
            notes='Test run',
        )

    def test_home_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/')

    def test_user_can_login(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'TestPassword123!',
            }
        )
        self.assertRedirects(response, reverse('home'))

    def test_logged_in_user_can_view_own_run(self):
        self.client.login(
            username='testuser',
            password='TestPassword123!'
        )
        response = self.client.get(reverse('home'))

        self.assertContains(response, '5.00')
        self.assertContains(response, 'Test run')

    def test_user_can_add_run(self):
        self.client.login(
            username='testuser',
            password='TestPassword123!'
        )
        response = self.client.post(
            reverse('home'),
            {
                'date': date.today(),
                'distance': 10.00,
                'distance_unit': 'km',
                'hours': 0,
                'minutes': 50,
                'seconds': 0,
                'run_type': 'Tempo',
                'notes': '10k tempo run',
            }
        )

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(
            Run.objects.filter(user=self.user, notes='10k tempo run').exists()
        )

    def test_user_can_edit_own_run(self):
        self.client.login(
            username='testuser',
            password='TestPassword123!'
        )
        response = self.client.post(
            reverse('edit_run', args=[self.run.id]),
            {
                'date': self.run.date,
                'distance': 6.00,
                'distance_unit': 'km',
                'hours': 0,
                'minutes': 35,
                'seconds': 0,
                'run_type': 'Easy',
                'notes': 'Updated test run',
            }
        )

        self.assertRedirects(response, reverse('home'))
        self.run.refresh_from_db()
        self.assertEqual(self.run.distance, 6.00)
        self.assertEqual(self.run.notes, 'Updated test run')

    def test_user_cannot_edit_another_users_run(self):
        self.client.login(
            username='otheruser',
            password='TestPassword123!'
        )
        # Testing POST attempt by unauthorized user
        response = self.client.post(
            reverse('edit_run', args=[self.run.id]),
            {
                'date': self.run.date,
                'distance': 10.00,
                'distance_unit': 'km',
                'hours': 1,
                'minutes': 0,
                'seconds': 0,
                'run_type': 'Easy',
                'notes': 'Hacked run',
            }
        )

        self.assertEqual(response.status_code, 404)
        self.run.refresh_from_db()
        self.assertNotEqual(self.run.distance, 10.00)

    def test_user_cannot_delete_another_users_run(self):
        self.client.login(
            username='otheruser',
            password='TestPassword123!'
        )
        response = self.client.post(
            reverse('delete_run', args=[self.run.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Run.objects.filter(id=self.run.id).exists()
        )

    def test_user_can_delete_own_run(self):
        self.client.login(
            username='testuser',
            password='TestPassword123!'
        )
        response = self.client.post(
            reverse('delete_run', args=[self.run.id])
        )

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(
            Run.objects.filter(id=self.run.id).exists()
        )

    def test_future_run_date_is_rejected(self):
        self.client.login(
            username='testuser',
            password='TestPassword123!'
        )

        future_date = date.today() + timedelta(days=1)

        response = self.client.post(
            reverse('home'),
            {
                'date': future_date,
                'distance': 5.00,
                'distance_unit': 'km',
                'hours': 0,
                'minutes': 30,
                'seconds': 0,
                'run_type': 'Easy',
                'notes': 'Future run',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'You cannot add a run in the future.'
        )

    def test_zero_duration_is_rejected(self):
        self.client.login(
            username='testuser',
            password='TestPassword123!'
        )

        response = self.client.post(
            reverse('home'),
            {
                'date': date.today(),
                'distance': 5.00,
                'distance_unit': 'km',
                'hours': 0,
                'minutes': 0,
                'seconds': 0,
                'run_type': 'Easy',
                'notes': 'Zero duration test',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Duration must be greater than 0.'
        )