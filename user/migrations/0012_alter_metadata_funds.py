# Generated by Django 4.2.8 on 2023-12-10 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_metadata_funds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadata',
            name='funds',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Funds'),
        ),
    ]
