# Generated by Django 3.2.3 on 2021-06-13 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='dis_image',
            field=models.ImageField(default='a', upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
