# Generated by Django 4.2.7 on 2023-12-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_rename_created_at_message_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='count',
            field=models.IntegerField(default=11),
            preserve_default=False,
        ),
    ]
