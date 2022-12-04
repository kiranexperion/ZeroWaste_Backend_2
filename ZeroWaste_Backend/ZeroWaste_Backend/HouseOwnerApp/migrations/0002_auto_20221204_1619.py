# Generated by Django 3.2.16 on 2022-12-04 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CorporationApp', '0001_initial'),
        ('HouseOwnerApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingstatus',
            name='wastecollector_id',
        ),
        migrations.AddField(
            model_name='bookingstatus',
            name='supervisor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CorporationApp.employee'),
        ),
    ]