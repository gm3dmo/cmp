from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Country(models.Model):
    # 3
    name = models.CharField(max_length=255, unique=True, default="")
    alpha2 = models.CharField(max_length=2, unique=True, default="")
    alpha3 = models.CharField(max_length=3, unique=True, default="")
    country_number = models.CharField(max_length=3, unique=True)
    flag = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("countries", args=[str(self.id)])


class Rank(models.Model):
    # 6
    name = models.CharField(max_length=50, unique=True)
    rank_types = (
        ("OR", "Other Rank"),
        ("NC", "Non Commisioned Officer"),
        ("OF", "Officer"),
    )
    abbreviation = models.CharField(max_length=50, blank=True)
    rank_class = models.CharField(
        max_length=2, blank=True, choices=rank_types, default="Other Rank"
    )

    def __str__(self):
        return self.name


class Cemetery(models.Model):
    # 1
    name = models.CharField(max_length=255, unique=True, default="")
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="cemeteries"
    )
    latitude = models.CharField(max_length=255, unique=False, default="")  # latitude
    longitude = models.CharField(max_length=255, unique=False, default="")  # longitude

    def __str__(self):
        return self.name


class PowCamp(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")
    nearest_city = models.CharField(max_length=255, unique=False, default="")
    notes = models.TextField(unique=False, default="")
    country = models.ForeignKey(
        "Country",
        to_field="country_number",
        on_delete=models.CASCADE,
        related_name="powcamps",
    )
    wartime_country = models.CharField(max_length=255, unique=False, default="")
    latitude = models.CharField(max_length=255, unique=False, default="")
    longitude = models.CharField(max_length=255, unique=False, default="")

    def __str__(self):
        return self.name


class Theatre(models.Model):
    # 11
    name = models.CharField(max_length=255, unique=True, default="")

    def __str__(self):
        return self.name


class Company(models.Model):
    # 2
    name = models.CharField(max_length=255, unique=True, default="")
    notes = models.TextField(unique=False, default="")

    def __str__(self):
        return self.name


class Decoration(models.Model):
    # 4
    name = models.CharField(max_length=255, unique=True, default="")
    notes = models.TextField(unique=False, default="")
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    details_link = models.CharField(max_length=255, unique=False, default="")
    abbreviation = models.CharField(max_length=255, unique=False, default="")

    def __str__(self):
        return self.name



class Soldier(models.Model):
    surname = models.CharField(max_length=255, unique=False, default="")
    initials = models.CharField(max_length=255, unique=False, default="")
    army_number = models.CharField(max_length=255, unique=False, default="")
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, related_name="ranks")
    notes = models.TextField(unique=False, default="")

    def __str__(self):
        return self.surname


class ProvostAppointment(models.Model):
    soldier = models.ForeignKey( Soldier, null=False, blank=False, on_delete=models.CASCADE)
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, related_name="provostappointments")
    date = models.DateField(null=True, blank=True)
    notes = models.TextField(unique=False, default="")

    def __str__(self):
        return self.rank


def get_upload_to(instance, filename):
    return f"""static/media/{instance.soldier_id}/memorial/{instance.soldier_id}.jpg""" 
 
 # http://localhost:8000/media/3774/memorial/3774.jpg
 # http://localhost:8000/static/media/3774/memorial/3774.jpg


class SoldierDeath(models.Model):
    soldier = models.OneToOneField(
        Soldier, on_delete=models.CASCADE, related_name="soldierdeath"
    )
    date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_to, null=True, blank=True)
    company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        default="UNKNOWN",
        on_delete=models.CASCADE,
        related_name="companies",
    )
    cemetery = models.ForeignKey(
        Cemetery,
        blank=True,
        null=True,
        default=110,
        on_delete=models.CASCADE,
        related_name="cemeteries",
    )
    cwgc_id = models.IntegerField(
        blank=True, null=True, unique=False, verbose_name="War Graves ID"
    )

    def __str__(self):
        return "%s %s %s" % (self.Soldier, self.date, self.cemetery)

    def cwgc_url(self):
        """Build a URL for a link to CWGC site."""
        wg_site = "http://www.cwgc.org"
        if self.cwgc_id:
            wg_string = "find-war-dead/casualty/%s/" % (self.cwgc_id)
            wg_url = "%s/%s" % (wg_site, wg_string)
            return wg_url
        else:
            dk = self.Date
            wg_string = (
                'search/SearchResults.aspx?surname=%s&initials=%s&war=0&yearfrom=%s&yearto=%s&force=%s&nationality=&send.x=26&send.y=19"'
                % (
                    self.Soldier.Surname,
                    self.Soldier.first_initial(),
                    dk.year,
                    dk.year,
                    "Army",
                )
            )
        wg_url = "%s/%s" % (wg_site, wg_string)
        return wg_url


class SoldierImprisonment(models.Model):
    soldier = models.ForeignKey("Soldier", on_delete=models.CASCADE)
    legacy_company = models.CharField(max_length=255, unique=False, default="")
    pow_number = models.CharField(max_length=255, unique=False, default="")
    pow_camp = models.ForeignKey("PowCamp", on_delete=models.CASCADE)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    legacy_date_from = models.CharField(max_length=255, unique=False, default="")
    legacy_date_to = models.CharField(max_length=255, unique=False, default="")
    notes = models.TextField(unique=False, default="")

    def __str__(self):
        return self.pow_camp.name


class SoldierDecoration(models.Model):
    soldier = models.ForeignKey(
        Soldier, null=False, blank=False, on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company, blank=True, null=True, on_delete=models.CASCADE
    )
    decoration = models.ForeignKey(
        Decoration, blank=True, null=True, on_delete=models.CASCADE
    )
    gazette_issue = models.CharField(max_length=50, blank=True)
    gazette_page = models.CharField(max_length=50, blank=True)
    gazette_date = models.DateField(null=True, blank=True)
    theatre = models.ForeignKey(
        Theatre,
        blank=True,
        null=True,
        help_text="Theatre of Operations e.g. Normandy, B.E.F. France & Flanders. NOT Country names",
        on_delete=models.CASCADE,
    )
    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.CASCADE
    )
    citation = models.TextField(max_length=50000, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.decoration.name

    def generate_gazette_url(self):
        """Build a URL for the London Gazette website. This will not handle Edinburgh gazette"""
        gz_site = "http://www.thegazette.co.uk"
        # "${gz_url}/SearchResults.aspx?GeoType=${gz_type}&st=${sc_type}&sb=issue&issue=${gz_issue}&gpn=${gz_page}&"
        gz_type = "london"
        sc_type = "adv"
        # gz_string = "SearchResults.aspx?GeoType=${gz_type}&st=${sc_type}&sb=issue&issue=${gz_issue}&gpn=${gz_page}&"
        gz_string = "%s/London/issue/%s/supplement/%s" % (
            gz_site,
            self.gazette_issue,
            self.gazette_page,
        )
        gazette_url = gz_string
        return gazette_url
