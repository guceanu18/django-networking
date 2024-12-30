# Generated by Django 4.2.2 on 2024-12-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Echipaement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.CharField(choices=[('router', 'Router'), ('switch', 'Switch')], max_length=50)),
                ('nume', models.CharField(max_length=100)),
                ('ip_adresa', models.GenericIPAddressField()),
                ('utilizator', models.CharField(max_length=50)),
                ('parola', models.CharField(max_length=50)),
            ],
        ),
    ]