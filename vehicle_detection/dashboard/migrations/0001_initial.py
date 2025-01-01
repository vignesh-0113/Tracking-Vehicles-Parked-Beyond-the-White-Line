# Generated by Django 5.1.4 on 2025-01-01 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_number', models.CharField(max_length=100)),
                ('license', models.CharField(default='UNKNOWN', max_length=100)),
                ('detection_time', models.DateTimeField()),
            ],
        ),
    ]
