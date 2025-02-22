import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from PIL import Image
from django.conf import settings

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
    alpha2 = models.CharField(max_length=2, unique=True, default="", blank=True)
    alpha3 = models.CharField(max_length=3, unique=True, default="", blank=True)
    country_number = models.CharField(max_length=3, unique=True)
    flag = models.CharField(max_length=255, default="", blank=True)

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
    latitude = models.CharField(max_length=255, unique=False, default="", blank=True)  # latitude
    longitude = models.CharField(max_length=255, unique=False, default="", blank=True)  # longitude

    def __str__(self):
        return self.name


class PowCamp(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")
    nearest_city = models.CharField(max_length=255, unique=False, default="", blank=True)
    notes = models.TextField(unique=False, default="", blank=True)
    country = models.ForeignKey(
        "Country",
        to_field="country_number",
        on_delete=models.CASCADE,
        related_name="powcamps",
    )
    wartime_country = models.CharField(max_length=255, unique=False, default="", blank=True)
    latitude = models.CharField(max_length=255, unique=False, default="", blank=True)
    longitude = models.CharField(max_length=255, unique=False, default="", blank=True)

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
    notes = models.TextField(unique=False, default="", blank=True)

    def __str__(self):
        return self.name


class Decoration(models.Model):
    # 4
    name = models.CharField(max_length=255, unique=True, default="")
    notes = models.TextField(unique=False, default="", blank=True)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    details_link = models.CharField(max_length=255, unique=False, default="", blank=True)
    abbreviation = models.CharField(max_length=255, unique=False, default="", blank=True)

    def __str__(self):
        return self.name


class Soldier(models.Model):
    surname = models.CharField(max_length=255, unique=False, default="")
    initials = models.CharField(max_length=255, unique=False, default="", blank=True)
    army_number = models.CharField(max_length=255, unique=False, default="", blank=True)
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, related_name="ranks")
    provost_officer = models.BooleanField(default=False)  
    notes = models.TextField(unique=False, default="", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['surname', 'initials']

    def first_initial(self):
        """Return the first initial of the soldier e.g. LC should return L"""
        if self.initials:
            return self.initials[0]
        else:
            return ""

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
    print("=== get_upload_to called ===")
    print(f"filename: {filename}")
    print(f"soldier_id: {instance.soldier_id}")
    return f'{instance.soldier_id}/memorial/{instance.soldier_id}.jpg'


class SoldierDeath(models.Model):
    soldier = models.OneToOneField(Soldier, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    cwgc_id = models.IntegerField(null=True, blank=True)
    cemetery = models.ForeignKey(Cemetery, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_to, null=True, blank=True)

    def save(self, *args, **kwargs):
        print("=== SoldierDeath save called ===")
        if self.image:
            print(f"Image present: {self.image}")
            print(f"Image path: {self.image.path if self.image else 'No path'}")
        super().save(*args, **kwargs)
        if self.image:
            print(f"Processing image at: {self.image.path}")
            img = Image.open(self.image.path)
            img.thumbnail((300, 400), Image.LANCZOS)
            img.save(self.image.path)

    def __str__(self):
        return "%s %s %s" % (self.soldier, self.date, self.cemetery)

    def cwgc_url(self):
        """Build a URL for a link to CWGC site."""
        if not self.date:  # Check if date is None
            return None  # or return a default URL
        wg_site = "http://www.cwgc.org"
        if self.cwgc_id:
            wg_string = "find-war-dead/casualty/%s/" % (self.cwgc_id)
            wg_url = "%s/%s" % (wg_site, wg_string)
            return wg_url
        else:
            dk = self.date
            wg_string = (
                'search/SearchResults.aspx?surname=%s&initials=%s&war=0&yearfrom=%s&yearto=%s&force=%s&nationality=&send.x=26&send.y=19"'
                % (
                    self.soldier.surname,
                    self.soldier.first_initial(),
                    dk.year,
                    dk.year,
                    "Army",
                )
            )
        wg_url = "%s/%s" % (wg_site, wg_string)
        return wg_url


class SoldierImprisonment(models.Model):
    soldier = models.ForeignKey("Soldier", on_delete=models.CASCADE)
    legacy_company = models.CharField(max_length=255, unique=False, default="", blank=True)
    pow_number = models.CharField(max_length=255, unique=False, default="", blank=True)
    pow_camp = models.ForeignKey("PowCamp", on_delete=models.CASCADE)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    legacy_date_from = models.CharField(max_length=255, unique=False, default="", blank=True)
    legacy_date_to = models.CharField(max_length=255, unique=False, default="", blank=True)
    notes = models.TextField(unique=False, default="", blank=True)

    def __str__(self):
        return self.pow_camp.name


class Acknowledgement(models.Model):
     surname = models.CharField(max_length=50, blank=True)
     name = models.CharField(max_length=50, blank=True)
     notes = models.TextField(max_length=50000, blank=True)
     last_modified = models.DateTimeField(auto_now=True)
     created_at = models.DateTimeField(default=timezone.now)
     def __str__(self) -> str:
         return self.surname


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
