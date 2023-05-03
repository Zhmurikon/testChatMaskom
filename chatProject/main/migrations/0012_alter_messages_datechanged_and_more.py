# Generated by Django 4.2 on 2023-05-03 03:20

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_alter_messages_datechanged_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='dateChanged',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 3, 13, 20, 40, 494076), null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='dateCreated',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 3, 13, 20, 40, 494076), null=True),
        ),
        migrations.CreateModel(
            name='UserLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateLoged', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
