# Generated by Django 3.2.3 on 2021-06-21 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='This-slug', unique=True),
            preserve_default=False,
        ),
    ]
