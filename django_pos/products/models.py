from django.db import models
from django.forms import model_to_dict
import django.utils.timezone


class Category(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )
    date_added = models.DateTimeField(default=django.utils.timezone.now)

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        # Table's name
        db_table = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the product",
    )
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.CASCADE, db_column='category')

    capacity = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(default=0)
    date_added = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        # Table's name
        db_table = "Product"

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        item = model_to_dict(self)
        item['id'] = self.id
        item['text'] = self.name
        item['category'] = self.category.name
        item['quantity'] = 1
        item['total_product'] = 0
        return item

class Store(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    products = models.ManyToManyField(Product, through='StoreInventory', related_name='stores')
    product_quantities = models.TextField(default="{}")  

    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name

    def update_product_quantity(self, product_id, quantity):
        """
        Update the quantity of a product in the store
        """
        # Parse the existing product quantities JSON string
        try:
            product_quantities = json.loads(self.product_quantities)
        except json.JSONDecodeError:
            product_quantities = {}

        # Update the quantity of the specified product
        product_quantities[str(product_id)] = quantity

        # Save the updated product quantities back to the model
        self.product_quantities = json.dumps(product_quantities, ensure_ascii=False)
        self.save()

        print(f"Updated product quantity for product ID {product_id} in store {self.name} to {quantity}.")

class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('store', 'product')

    def __str__(self):
        return f'{self.store} {self.product} {self.quantity}'

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(default=django.utils.timezone.now)
    address = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class Purchase(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} at {self.store.name} ({self.quantity})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        store_inventory, created = StoreInventory.objects.get_or_create(store=self.store, product=self.product)
        store_inventory.quantity += self.quantity
        store_inventory.save()