# Generated by Django 4.2 on 2023-05-04 04:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0013_alter_messages_datechanged_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='dateChanged',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 4, 14, 39, 23, 473618), null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='dateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 4, 14, 39, 23, 473618), null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
