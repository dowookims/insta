# Generated by Django 2.1.7 on 2019-04-18 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
