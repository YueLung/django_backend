# Generated by Django 4.0.6 on 2022-07-26 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trial', '0002_productcategory_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('created_at',)},
        ),
    ]