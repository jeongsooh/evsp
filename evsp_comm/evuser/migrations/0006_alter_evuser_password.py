# Generated by Django 4.0.4 on 2022-05-26 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evuser', '0005_alter_evuser_category_alter_evuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='비밀번호'),
        ),
    ]