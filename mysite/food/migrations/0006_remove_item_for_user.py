# Generated by Django 5.0 on 2024-01-06 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_item_for_user_item_prod_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='for_user',
        ),
    ]
