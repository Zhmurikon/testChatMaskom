# Generated by Django 4.2 on 2023-05-10 03:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_messages_datechanged_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='dateChanged',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 10, 13, 43, 14, 60774), null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='dateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 13, 43, 14, 60774), null=True),
        ),
    ]
