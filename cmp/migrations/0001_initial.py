# Generated by Django 5.1.6 on 2025-03-20 07:18

import cmp.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Acknowledgement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("surname", models.CharField(blank=True, max_length=50)),
                ("name", models.CharField(blank=True, max_length=50)),
                ("notes", models.TextField(blank=True, max_length=50000)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=255, unique=True)),
                ("notes", models.TextField(blank=True, default="")),
            ],
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=255, unique=True)),
                (
                    "alpha2",
                    models.CharField(blank=True, default="", max_length=2, unique=True),
                ),
                (
                    "alpha3",
                    models.CharField(blank=True, default="", max_length=3, unique=True),
                ),
                ("country_number", models.CharField(max_length=3, unique=True)),
                ("flag", models.CharField(blank=True, default="", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Rank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("abbreviation", models.CharField(blank=True, max_length=50)),
                (
                    "rank_class",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("OR", "Other Rank"),
                            ("NC", "Non Commisioned Officer"),
                            ("OF", "Officer"),
                        ],
                        default="Other Rank",
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Theatre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("username", models.CharField(max_length=150, unique=True)),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Cemetery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=255, unique=True)),
                ("latitude", models.CharField(blank=True, default="", max_length=255)),
                ("longitude", models.CharField(blank=True, default="", max_length=255)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cemeteries",
                        to="cmp.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Decoration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=255, unique=True)),
                ("notes", models.TextField(blank=True, default="")),
                (
                    "details_link",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "abbreviation",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cmp.country"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PowCamp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=255, unique=True)),
                (
                    "nearest_city",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("notes", models.TextField(blank=True, default="")),
                (
                    "wartime_country",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("latitude", models.CharField(blank=True, default="", max_length=255)),
                ("longitude", models.CharField(blank=True, default="", max_length=255)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="powcamps",
                        to="cmp.country",
                        to_field="country_number",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Soldier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("surname", models.CharField(default="", max_length=255)),
                ("initials", models.CharField(blank=True, default="", max_length=255)),
                (
                    "army_number",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("provost_officer", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "rank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ranks",
                        to="cmp.rank",
                    ),
                ),
            ],
            options={
                "ordering": ["surname", "initials"],
            },
        ),
        migrations.CreateModel(
            name="ProvostAppointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(default="")),
                (
                    "rank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="provostappointments",
                        to="cmp.rank",
                    ),
                ),
                (
                    "soldier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cmp.soldier"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SoldierDeath",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("cwgc_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=cmp.models.get_upload_to
                    ),
                ),
                (
                    "cemetery",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cmp.cemetery",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cmp.company",
                    ),
                ),
                (
                    "soldier",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="cmp.soldier"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SoldierImprisonment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "legacy_company",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "pow_number",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("date_from", models.DateField(blank=True, null=True)),
                ("date_to", models.DateField(blank=True, null=True)),
                (
                    "legacy_date_from",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "legacy_date_to",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("notes", models.TextField(blank=True, default="")),
                (
                    "pow_camp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cmp.powcamp"
                    ),
                ),
                (
                    "soldier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cmp.soldier"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SoldierDecoration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gazette_issue", models.CharField(blank=True, max_length=50)),
                ("gazette_page", models.CharField(blank=True, max_length=50)),
                ("gazette_date", models.DateField(blank=True, null=True)),
                ("citation", models.TextField(blank=True, max_length=50000)),
                ("notes", models.TextField(blank=True)),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cmp.company",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cmp.country",
                    ),
                ),
                (
                    "decoration",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cmp.decoration",
                    ),
                ),
                (
                    "soldier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cmp.soldier"
                    ),
                ),
                (
                    "theatre",
                    models.ForeignKey(
                        blank=True,
                        help_text="Theatre of Operations e.g. Normandy, B.E.F. France & Flanders. NOT Country names",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cmp.theatre",
                    ),
                ),
            ],
        ),
    ]
