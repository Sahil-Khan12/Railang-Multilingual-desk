# Generated by Django 4.1.13 on 2023-11-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Train",
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
                ("Train_no", models.IntegerField()),
                ("Train_Name", models.CharField(max_length=150)),
                ("Arival_time", models.CharField(max_length=50)),
                ("Departure", models.CharField(max_length=100)),
                ("Origin", models.CharField(max_length=100)),
                ("Destination", models.CharField(max_length=100)),
                ("Day", models.CharField(max_length=100)),
            ],
        ),
    ]