# Generated by Django 5.2.1 on 2025-05-28 10:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_salesnetworkcell_hierarchy_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salesnetworkcell",
            name="hierarchy_level",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)],
                verbose_name="Hierarchy Level",
            ),
        ),
        migrations.AlterField(
            model_name="salesnetworkcell",
            name="hierarchy_name",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Factory", "Factory"),
                    ("Retail Network", "Retail Network"),
                    ("Individual Entrepreneur", "Individual Entrepreneur"),
                ],
                max_length=100,
                verbose_name="Hierarchy Name",
            ),
        ),
    ]
