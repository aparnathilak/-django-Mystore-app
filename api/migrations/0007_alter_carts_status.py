# Generated by Django 4.1.2 on 2023-01-12 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_carts_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carts',
            name='status',
            field=models.CharField(choices=[('Order-placed', 'Order-placed'), ('In-cart', 'In-cart'), ('Cancelled', 'Cancelled')], default='In-cart', max_length=200),
        ),
    ]