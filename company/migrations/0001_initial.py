# Generated by Django 4.2 on 2024-05-07 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
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
                ("symbol_val", models.CharField(max_length=10, unique=True)),
                ("title", models.TextField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Companies",
            },
        ),
        migrations.CreateModel(
            name="StockInfo",
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
                ("date", models.DateField()),
                ("Open", models.FloatField()),
                ("High", models.FloatField()),
                ("Low", models.FloatField()),
                ("Close", models.FloatField()),
                ("Adj_Close", models.FloatField()),
                ("Volume", models.BigIntegerField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "symbol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="company.company",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Stock Information",
            },
        ),
        migrations.CreateModel(
            name="CompanyMetric",
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
                ("date_min", models.DateTimeField()),
                ("date_max", models.DateTimeField()),
                ("last_updated", models.DateTimeField(auto_now_add=True)),
                (
                    "symbol",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="company.company",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Company Metrics",
            },
        ),
    ]
