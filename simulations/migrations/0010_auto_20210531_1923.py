# Generated by Django 3.0.4 on 2021-05-31 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0009_simulation_main_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='url',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
