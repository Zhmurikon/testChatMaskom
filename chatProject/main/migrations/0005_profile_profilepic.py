# Generated by Django 4.2 on 2023-05-02 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
