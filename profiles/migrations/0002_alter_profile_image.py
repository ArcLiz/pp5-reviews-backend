# Generated by Django 3.2.25 on 2024-06-04 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../default_profile_xwtjlx', upload_to='images/'),
        ),
    ]
