import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase

from cmp.views import original_unit, belongsTo

from cmp.models import Rank
from cmp.models import Soldier
from cmp.models import Country
from cmp.models import Cemetery
from cmp.models import Decoration
from cmp.models import SoldierDecoration
from cmp.models import SoldierDeath
from cmp.models import SoldierImprisonment
from cmp.models import PowCamp


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
class DecorationModelTest(TestCase):
    def test_create_decoration(self):
        name = "Decoration1"
        notes = "Decoration1 notes"
        details_link = "https://www.example.com"
        abbreviation = "D1"
        country_name = "UNKNOWN"
        country, created = Country.objects.get_or_create(name=country_name)
        decoration = Decoration.objects.create(name=name, country=country, notes=notes, details_link=details_link, abbreviation=abbreviation)
        self.assertEqual(decoration.name, name)
        self.assertEqual(str(decoration.name), name)

@pytest.mark.django_db
class SoldierModelTest(TestCase):
    def test_create_soldier(self):
        surname = "Soldier1"
        initials = "AB"
        army_number = 12345678
        rank, created = Rank.objects.get_or_create(name="Private", abbreviation="Pte", rank_class="Other Rank")
        soldier = Soldier.objects.create(surname=surname, initials=initials, army_number=army_number, rank=rank)
        self.assertEqual(soldier.surname, surname)
        self.assertEqual(str(soldier.surname), surname)


@pytest.mark.django_db
class SoldierDecorationModelTest(TestCase):
    def test_create_soldier_decoration(self):
        name = "Decoration1"
        notes = "Decoration1 notes"
        details_link = "https://www.example.com"
        abbreviation = "D1"
        country_name = "UNKNOWN"
        country, created = Country.objects.get_or_create(name=country_name)
        decoration = Decoration.objects.create(name=name, country=country, details_link=details_link, abbreviation=abbreviation)
        soldier = Soldier.objects.create(surname="Soldier1", initials="AB", army_number=12345678, rank=Rank.objects.get_or_create(name="Private", abbreviation="Pte", rank_class="Other Rank")[0])
        soldier_decoration = SoldierDecoration.objects.create(decoration=decoration, soldier=soldier, citation="Citation1", gazette_issue=1, gazette_page=1)
        gazette_url = soldier_decoration.generate_gazette_url()

        self.assertEqual(soldier_decoration.decoration, decoration) 
        self.assertEqual(gazette_url, "http://www.thegazette.co.uk/London/issue/1/supplement/1")


#@pytest.mark.django_db
#class SoldierDeathModelTest(TestCase):
#    def test_create_soldier_death(self):
#        soldier = Soldier.objects.create(surname="Soldier1", initials="AB", army_number=12345678, rank=Rank.objects.get_or_create(name="Private", abbreviation="Pte", rank_class="Other Rank")[0])
#        country_name = "UNKNOWN"
#        country, created = Country.objects.get_or_create(name=country_name)
#        cemetery = Cemetery.objects.create(name="Cemetery1", latitude=1.0, longitude=1.0, country=country)
#        for field in cemetery._meta.fields:
#            print(f"{field.name}: {getattr(cemetery, field.name)}")
#        print(type(cemetery))
#        print(type(soldier))
#        try:
#            soldier_death = SoldierDeath.objects.create(soldier=soldier, cemetery=1)
#        except ValueError as e:
#            print(e)
#        soldier_death = SoldierDeath.objects.create(soldier=soldier, cemetery=cemetery)
#        #soldier_death = SoldierDeath.objects.create(soldier=soldier, cemetery=cemetery)
#        #self.assertEqual(soldier_death.soldier, soldier)


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
class CountryModelTest(TestCase):
    def test_create_country(self):
        name = "Country1"
        country = Country.objects.create(name=name)
        self.assertEqual(country.name, name)    


@pytest.mark.django_db
class CemeteryModelTest(TestCase):
    def test_create_cemetery(self):
        name = "Cemetery1"
        latitude = 1.0
        longitude = 1.0
        country_name  = "UNKNOWN"
        country, created = Country.objects.get_or_create(name=country_name)
        cemetery = Cemetery.objects.create(name=name, latitude=latitude, longitude=longitude, country=country)
        self.assertEqual(cemetery.name, name)


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
    
    #def test_index_view(self):
    #    response = self.client.get("/")
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTemplateUsed(response, "cmp/index.html")

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cmp/soldier-results.html")