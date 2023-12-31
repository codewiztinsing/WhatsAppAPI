# Generated by Django 4.2.7 on 2023-12-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_chatroom_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='count',
            new_name='active_client',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='max_client',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
