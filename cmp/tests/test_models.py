from django.test import TestCase
from django.utils import timezone
from cmp.models import (
    CustomUser, Country, Rank, Cemetery, PowCamp, Theatre,
    Company, Decoration, Soldier, ProvostAppointment,
    SoldierDeath, SoldierImprisonment, Acknowledgement,
    SoldierDecoration
)

class CustomUserTests(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create(email="test@example.com")
        self.assertEqual(str(user), "test@example.com")

class CountryTests(TestCase):
    def test_country_creation(self):
        country = Country.objects.create(
            name="Test Country",
            alpha2="TC",
            alpha3="TCY",
            country_number="999",
            flag="flag.png"
        )
        self.assertEqual(str(country), "Test Country")
        self.assertEqual(country.get_absolute_url(), "/mgmt/countries/1/")

class RankTests(TestCase):
    def test_rank_creation(self):
        rank = Rank.objects.create(
            name="Sergeant",
            abbreviation="Sgt",
            rank_class="NC"
        )
        self.assertEqual(str(rank), "Sergeant")

class CemeteryTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country", country_number="999")

    def test_cemetery_creation(self):
        cemetery = Cemetery.objects.create(
            name="Test Cemetery",
            country=self.country,
            latitude="51.5074",
            longitude="-0.1278"
        )
        self.assertEqual(str(cemetery), "Test Cemetery")

class PowCampTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country", country_number="999")

    def test_powcamp_creation(self):
        camp = PowCamp.objects.create(
            name="Test Camp",
            country=self.country,
            nearest_city="Test City",
            wartime_country="Test Wartime Country",
            latitude="51.5074",
            longitude="-0.1278"
        )
        self.assertEqual(str(camp), "Test Camp")

class TheatreTests(TestCase):
    def test_theatre_creation(self):
        theatre = Theatre.objects.create(name="Test Theatre")
        self.assertEqual(str(theatre), "Test Theatre")

class CompanyTests(TestCase):
    def test_company_creation(self):
        company = Company.objects.create(
            name="Test Company",
            notes="Test Notes"
        )
        self.assertEqual(str(company), "Test Company")

class DecorationTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country", country_number="999")

    def test_decoration_creation(self):
        decoration = Decoration.objects.create(
            name="Test Decoration",
            country=self.country,
            abbreviation="TD",
            details_link="http://example.com"
        )
        self.assertEqual(str(decoration), "Test Decoration")

class SoldierTests(TestCase):
    def setUp(self):
        self.rank = Rank.objects.create(name="Private")

    def test_soldier_creation(self):
        soldier = Soldier.objects.create(
            surname="Smith",
            initials="J.A.",
            army_number="12345",
            rank=self.rank
        )
        self.assertEqual(str(soldier), "Smith")
        self.assertEqual(soldier.first_initial(), "J")

class ProvostAppointmentTests(TestCase):
    def setUp(self):
        self.rank = Rank.objects.create(name="Sergeant")
        self.soldier = Soldier.objects.create(
            surname="Smith",
            rank=self.rank
        )

    def test_provost_appointment_creation(self):
        appointment = ProvostAppointment.objects.create(
            soldier=self.soldier,
            rank=self.rank,
            date=timezone.now().date()
        )
        self.assertEqual(str(appointment), "Sergeant")

class SoldierDeathTests(TestCase):
    def setUp(self):
        self.rank = Rank.objects.create(name="Private")
        self.soldier = Soldier.objects.create(
            surname="Smith",
            rank=self.rank
        )

    def test_soldier_death_creation(self):
        death = SoldierDeath.objects.create(
            soldier=self.soldier,
            date=timezone.now().date()
        )
        self.assertEqual(str(death), "Smith - " + str(timezone.now().date()))

class SoldierImprisonmentTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country", country_number="999")
        self.rank = Rank.objects.create(name="Private")
        self.soldier = Soldier.objects.create(
            surname="Smith",
            rank=self.rank
        )
        self.pow_camp = PowCamp.objects.create(
            name="Test Camp",
            country=self.country
        )

    def test_imprisonment_creation(self):
        imprisonment = SoldierImprisonment.objects.create(
            soldier=self.soldier,
            pow_camp=self.pow_camp,
            pow_number="12345"
        )
        self.assertEqual(str(imprisonment), "Test Camp")

class AcknowledgementTests(TestCase):
    def test_acknowledgement_creation(self):
        ack = Acknowledgement.objects.create(
            surname="Smith",
            name="John Smith",
            notes="Test acknowledgement"
        )
        self.assertEqual(str(ack), "Smith")

class SoldierDecorationTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country", country_number="999")
        self.rank = Rank.objects.create(name="Private")
        self.soldier = Soldier.objects.create(
            surname="Smith",
            rank=self.rank
        )
        self.decoration = Decoration.objects.create(
            name="Test Decoration",
            country=self.country
        )

    def test_decoration_creation(self):
        decoration = SoldierDecoration.objects.create(
            soldier=self.soldier,
            decoration=self.decoration,
            gazette_issue="12345",
            gazette_page="678"
        )
        self.assertEqual(str(decoration), "Test Decoration")

    def test_generate_gazette_url(self):
        decoration = SoldierDecoration.objects.create(
            soldier=self.soldier,
            decoration=self.decoration,
            gazette_issue="12345",
            gazette_page="678"
        )
        expected_url = "http://www.thegazette.co.uk/London/issue/12345/supplement/678"
        self.assertEqual(decoration.generate_gazette_url(), expected_url) 