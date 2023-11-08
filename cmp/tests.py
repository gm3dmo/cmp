import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase

from cmp.views import original_unit, belongsTo

from cmp.models import Rank

from cmp import views

class TestOriginalUnit(TestCase):

    def test_original_unit_with_input_0(self):
        # Define the input
        input_value = 0

        # Define the expected output
        expected_output = "No Match Found"

        # Call the original_unit function with the input
        result = original_unit(None, input_value)

        # Use assert to check if the result matches the expected output
        self.assertContains(result, expected_output)

    def test_original_unit_with_input_2(self):
        # Define the input
        input_value = 2

        # Define the expected output
        expected_output = "Royal Army Service Corps (Block 1)"

        # Call the original_unit function with the input
        result = original_unit(None, input_value)

        # Use assert to check if the result matches the expected output
        self.assertContains(result, expected_output)


    def test_original_unit_with_input_7875698(self):
        # Define the input
        input_value = 7875698

        # Define the expected output
        expected_output = "Royal Tank Regiment"

        # Call the original_unit function with the input
        result = original_unit(None, input_value)

        # Use assert to check if the result matches the expected output
        self.assertContains(result, expected_output)



    def test_original_unit_with_input_1(self):
        # Define the input
        input_value = 1

        # Define the expected output
        expected_output = "Royal Army Service Corps (Block 1)"

        # Call the original_unit function with the input
        result = original_unit(None, input_value)

        # Use assert to check if the result matches the expected output
        self.assertContains(result, expected_output)


    def test_original_unit_with_input_22199408(self):
        # Define the input
        input_value = 22199408

        # Define the expected output
        expected_output = "Until October 1950"

        # Call the original_unit function with the input
        result = original_unit(None, input_value)

        # Use assert to check if the result matches the expected output
        self.assertContains(result, expected_output)


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        expected_email = "normal@user.com"
        user = User.objects.create_user(email=expected_email, password="foo")
        self.assertEqual(user.email, expected_email)
        self.assertEqual(user.__str__(), expected_email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo",  is_staff=False
            )

    


@pytest.mark.django_db
class RankModelTest(TestCase):
    def test_create_rank(self):
        name = "Private"
        abbreviation = "Pte"
        rank_class = "Other Rank"
        rank = Rank.objects.create(name=name, abbreviation=abbreviation, rank_class=rank_class)
        self.assertEqual(rank.name, name)
        self.assertEqual(rank.abbreviation, abbreviation)
        self.assertEqual(rank.rank_class, rank_class)
        self.assertEqual(str(rank), name)

@pytest.mark.django_db
class testViewsModule(TestCase):
    def test_powcamps_view(self):
        response = self.client.get("/pow-camps/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cmp/pow-camps.html")

    def test_cemeteries_view(self):
        response = self.client.get("/cemeteries/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cmp/cemeteries.html")

    def test_ranks_view(self):
        response = self.client.get("/ranks/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cmp/ranks.html")

    def test_countries_view(self):
        response = self.client.get("/countries/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cmp/countries.html")
    
    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cmp/index.html")
