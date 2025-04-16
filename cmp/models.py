import os
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from PIL import Image
from django.conf import settings
from io import BytesIO
from django.core.files import File
from datetime import datetime

from .managers import CustomUserManager
from pathlib import Path


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


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
    soldier = models.ForeignKey(Soldier, null=False, blank=False, on_delete=models.CASCADE)
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, related_name="provostappointments")
    date = models.DateField(null=True, blank=True)
    notes = models.TextField(unique=False, default="")

    def __str__(self):
        return self.rank.name  # Return the name string directly


def get_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    base_path = f'{instance.soldier.id}/memorial'
    base_name = f'{instance.soldier.id}{ext}'
    relative_path = f'{base_path}/{base_name}'
    
    # If this is a new file being uploaded
    if hasattr(instance.image, 'file'):
        print("Processing new image upload")
        
        # Check if file already exists
        full_path = os.path.join(settings.MEDIA_ROOT, base_path, base_name)
        if os.path.exists(full_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'{instance.soldier.id}_{timestamp}{ext}'
            backup_path = os.path.join(settings.MEDIA_ROOT, base_path, backup_name)
            os.rename(full_path, backup_path)
            print(f"Moved existing file to {backup_path}")
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Process and save the new image
        with Image.open(instance.image) as img:
            print(f"Original size: {img.size}")
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.thumbnail((300, 400), Image.LANCZOS)
            print(f"New size after thumbnail: {img.size}")
            # Save directly to the final location
            img.save(full_path, 'JPEG', quality=85)
            print(f"Saved resized image to {full_path}")
    
    return relative_path


class SoldierDeath(models.Model):
    soldier = models.OneToOneField(Soldier, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    cemetery = models.ForeignKey(Cemetery, on_delete=models.SET_NULL, null=True, blank=True)
    cwgc_id = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_to, null=True, blank=True)

    def save(self, *args, **kwargs):
        print("\n=== SoldierDeath save called ===")
        if self.image:
            print(f"Image name: {self.image.name}")
            print(f"Image path: {self.image.path if hasattr(self.image, 'path') else 'No path yet'}")
            print(f"Image URL: {self.image.url if hasattr(self.image, 'url') else 'No URL yet'}")
        super().save(*args, **kwargs)
        if self.image:
            print(f"After save - Image path: {self.image.path}")
            print(f"File exists: {os.path.exists(self.image.path)}")

    def __str__(self):
        return f"{self.soldier} - {self.date}"

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
