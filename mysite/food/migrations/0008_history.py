# Generated by Django 5.0 on 2024-01-31 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_item_added_by_item_rest_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='username', max_length=50)),
                ('prod_code', models.IntegerField(default=100)),
                ('item_name', models.CharField(default='itemname', max_length=50)),
                ('operations_type', models.CharField(default='optyp', max_length=50)),
            ],
        ),
    ]