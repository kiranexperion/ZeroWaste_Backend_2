# Generated by Django 3.2.16 on 2022-12-03 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CorporationApp', '0002_employee_roles_wastecollector'),
        ('HouseOwnerApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookingstatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=200)),
                ('collection_date', models.DateField(null=True)),
                ('booking_date', models.DateField()),
                ('slot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HouseOwnerApp.slotbooking')),
                ('wastecollector_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CorporationApp.wastecollector')),
            ],
        ),
    ]
