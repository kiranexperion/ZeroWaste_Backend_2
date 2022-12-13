# Generated by Django 3.2.16 on 2022-12-12 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CorporationApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='houseowner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('phoneno', models.CharField(max_length=200, unique=True)),
                ('address', models.CharField(max_length=1000)),
                ('pincode', models.CharField(max_length=50)),
                ('wardno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CorporationApp.wards')),
            ],
        ),
        migrations.CreateModel(
            name='slotbooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('quantity', models.FloatField()),
                ('payment_status', models.BooleanField(default=0)),
                ('houseowner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HouseOwnerApp.houseowner')),
                ('waste_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CorporationApp.wastes')),
            ],
        ),
        migrations.CreateModel(
            name='paymentstatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_paydate', models.DateField()),
                ('houseowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HouseOwnerApp.houseowner')),
            ],
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalamount', models.FloatField()),
                ('pay_date', models.DateField()),
                ('houseowner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HouseOwnerApp.houseowner')),
            ],
        ),
        migrations.CreateModel(
            name='bookingstatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=200)),
                ('collection_date', models.DateField(null=True)),
                ('booking_date', models.DateField()),
                ('slot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HouseOwnerApp.slotbooking')),
                ('supervisor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CorporationApp.employee')),
            ],
        ),
    ]
