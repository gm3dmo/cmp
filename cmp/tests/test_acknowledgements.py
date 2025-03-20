import pytest
from django.test import TestCase
from django.urls import reverse
from cmp.models import Acknowledgement
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class AcknowledgementModelTest(TestCase):
    def test_create_acknowledgement(self):
        name = "John"
        surname = "Smith"
        notes = "Test acknowledgement"
        acknowledgement = Acknowledgement.objects.create(
            name=name,
            surname=surname,
            notes=notes
        )
        self.assertEqual(acknowledgement.name, name)
        self.assertEqual(acknowledgement.surname, surname)
        self.assertEqual(acknowledgement.notes, notes)
        # Updated to match your model's actual __str__ method
        self.assertEqual(str(acknowledgement), surname)  # Just expects "Smith"

@pytest.mark.django_db
class AcknowledgementViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        User = get_user_model()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',  # Add username
            password='testpassword',
            is_staff=True  # Make sure user has permissions
        )
        
        # Create a test acknowledgement
        self.acknowledgement = Acknowledgement.objects.create(
            name='John',
            # Add any other required fields
        )
        
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        # Or if your app uses email for login:
        # self.client.login(email='testuser@example.com', password='testpassword')

    def test_search_acknowledgement_view(self):
        response = self.client.get('/mgmt/acknowledgement/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmp/search-acknowledgement.html')

    def test_edit_acknowledgement_view_get(self):
        response = self.client.get(f'/mgmt/acknowledgement/edit/{self.acknowledgement.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmp/edit-acknowledgement.html')

    def test_edit_acknowledgement_view_post(self):
        updated_data = {
            'name': 'Jane',
            'surname': 'Doe',
            'notes': 'Updated notes'
        }
        response = self.client.post(
            f'/mgmt/acknowledgement/edit/{self.acknowledgement.id}/',
            updated_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify the update
        updated_acknowledgement = Acknowledgement.objects.get(id=self.acknowledgement.id)
        self.assertEqual(updated_acknowledgement.name, 'Jane')
        self.assertEqual(updated_acknowledgement.surname, 'Doe')
        self.assertEqual(updated_acknowledgement.notes, 'Updated notes') 