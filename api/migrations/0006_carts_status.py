# Generated by Django 4.1.2 on 2023-01-11 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='carts',
            name='status',
            field=models.CharField(choices=[('Order-placed', 'Order-placed'), ('In-cart', 'In-cart'), ('Cancelled', 'Cancelled')], default='Order-placed', max_length=200),
        ),
    ]
