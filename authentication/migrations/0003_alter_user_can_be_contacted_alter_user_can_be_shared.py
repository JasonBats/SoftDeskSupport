# Generated by Django 5.0.4 on 2024-04-23 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_can_be_sharde_user_can_be_shared'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='can_be_contacted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='can_be_shared',
            field=models.BooleanField(default=False),
        ),
    ]
