# Generated by Django 4.0.4 on 2022-05-12 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evcharger', '0001_initial'),
        ('charginginfo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charginginfo',
            name='cpnumber',
        ),
        migrations.AddField(
            model_name='charginginfo',
            name='cpname',
            field=models.ForeignKey(default='100', on_delete=django.db.models.deletion.CASCADE, to='evcharger.evcharger', verbose_name='충전기이름'),
            preserve_default=False,
        ),
    ]