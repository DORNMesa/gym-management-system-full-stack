# Generated by Django 4.2.8 on 2023-12-10 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0002_coach_due_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='ref',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Reference'),
        ),
    ]
