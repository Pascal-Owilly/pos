# Generated by Django 4.1.5 on 2024-05-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_customuser_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
