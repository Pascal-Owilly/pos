# Generated by Django 4.1.5 on 2024-05-17 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_inventory_store_products'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Inventory',
            new_name='StoreInventory',
        ),
        migrations.AlterUniqueTogether(
            name='storeinventory',
            unique_together={('store', 'product')},
        ),
    ]
