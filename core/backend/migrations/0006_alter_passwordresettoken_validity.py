# Generated by Django 4.2.6 on 2023-11-01 18:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_remove_passwordresettoken_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='validity',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
