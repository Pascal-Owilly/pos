# Generated by Django 4.1.5 on 2024-05-16 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('address', models.TextField(blank=True, max_length=256, null=True)),
                ('email', models.EmailField(blank=True, max_length=256, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'Suppliers',
            },
        ),
    ]
