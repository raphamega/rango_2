# Generated by Django 4.2.3 on 2023-07-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_texto'),
    ]

    operations = [
        migrations.AddField(
            model_name='texto',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='text_image/'),
        ),
    ]
