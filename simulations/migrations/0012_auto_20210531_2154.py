# Generated by Django 3.0.4 on 2021-05-31 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0011_auto_20210531_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='state',
            field=models.IntegerField(choices=[(1, 'Initial'), (2, 'Fluid'), (3, 'Ipr'), (4, 'Well'), (5, 'Separator'), (6, 'Rod'), (7, 'Pumpunit'), (8, 'Surfaceequipment')], default=1),
        ),
    ]
