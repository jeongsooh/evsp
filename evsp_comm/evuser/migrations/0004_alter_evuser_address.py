# Generated by Django 4.0.4 on 2022-05-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evuser', '0003_evuser_address_evuser_category_evuser_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evuser',
            name='address',
            field=models.TextField(verbose_name='주소'),
        ),
    ]
