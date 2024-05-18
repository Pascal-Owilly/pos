from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Product, StoreInventory
from django.shortcuts import render, get_object_or_404

@login_required(login_url="/accounts/login/")
def CategoriesListView(request):
    context = {
        "active_icon": "products_categories",
        "categories": Category.objects.all().order_by('-date_added')
    }
    return render(request, "products/categories.html", context=context)


@login_required(login_url="/accounts/login/")
def CategoriesAddView(request):
    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }

        # Check if a category with the same attributes exists
        if Category.objects.filter(**attributes).exists():
            messages.error(request, 'Category already exists!',
                           extra_tags="warning")
            return redirect('products:categories_add')

        try:
            # Create the category
            new_category = Category.objects.create(**attributes)

            # If it doesn't exists save it
            new_category.save()

            messages.success(request, 'Category: ' +
                             attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:categories_add')

    return render(request, "products/categories_add.html", context=context)


@login_required(login_url="/accounts/login/")
def CategoriesUpdateView(request, category_id):
    """
    Args:
        category_id : The category's ID that will be updated
    """

    # Get the category
    try:
        # Get the category to update
        category = Category.objects.get(id=category_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the category!', extra_tags="danger")
        print(e)
        return redirect('products:categories_list')

    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices,
        "category": category
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description']
            }

            # Check if a category with the same attributes exists
            if Category.objects.filter(**attributes).exists():
                messages.error(request, 'Category already exists!',
                               extra_tags="warning")
                return redirect('products:categories_add')

            # Get the category to update
            category = Category.objects.filter(
                id=category_id).update(**attributes)

            category = Category.objects.get(id=category_id)

            messages.success(request, '¡Category: ' + category.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the elimination!', extra_tags="danger")
            print(e)
            return redirect('products:categories_list')

    return render(request, "products/categories_update.html", context=context)


@login_required(login_url="/accounts/login/")
def CategoriesDeleteView(request, category_id):
    """
    Args:
        category_id : The category's ID that will be deleted
    """
    try:
        # Get the category to delete
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, '¡Category: ' + category.name +
                         ' deleted!', extra_tags="success")
        return redirect('products:categories_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('products:categories_list')


@login_required(login_url="/accounts/login/")
def ProductsListView(request):
    context = {
        "active_icon": "products",
        "products": Product.objects.all().order_by('-date_added')
    }
    return render(request, "products/products.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsAddView(request):
    context = {
        "active_icon": "products_categories",
        "product_status": Product.status.field.choices,
        "categories": Category.objects.all().filter(status="ACTIVE")
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description'],
            "category": Category.objects.get(id=data['category']),
            "price": data['price'],
            "capacity": data['capacity']
        }

        # Check if a product with the same attributes exists
        if Product.objects.filter(**attributes).exists():
            messages.error(request, 'Product already exists!',
                           extra_tags="warning")
            return redirect('products:products_add')

        try:
            # Create the product
            new_product = Product.objects.create(**attributes)

            # If it doesn't exists save it
            new_product.save()

            messages.success(request, 'Product: ' +
                             attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:products_add')

    return render(request, "products/products_add.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsUpdateView(request, product_id):
    """
    Args:
        product_id : The product's ID that will be updated
    """

    # Get the product
    try:
        # Get the product to update
        product = Product.objects.get(id=product_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the product!', extra_tags="danger")
        print(e)
        return redirect('products:products_list')

    context = {
        "active_icon": "products",
        "product_status": Product.status.field.choices,
        "product": product,
        "categories": Category.objects.all()
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description'],
                "category": Category.objects.get(id=data['category']),
                "price": data['price']
            }

            # Check if a product with the same attributes exists
            if product.objects.filter(**attributes).exists():
                messages.error(request, 'Product already exists!',
                               extra_tags="warning")
                return redirect('products:products_add')

            # Get the product to update
            product = Product.objects.filter(
                id=product_id).update(**attributes)

            product = Product.objects.get(id=product_id)

            messages.success(request, '¡Product: ' + product.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('products:products_list')

    return render(request, "products/products_update.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsDeleteView(request, product_id):
    """
    Args:
        product_id : The product's ID that will be deleted
    """
    try:
        # Get the product to delete
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, '¡Product: ' + product.name +
                         ' deleted!', extra_tags="success")
        return redirect('products:products_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('products:products_list')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def GetProductsAJAXView(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []

            products = Product.objects.filter(
                name__icontains=request.POST['term'])
            for product in products[0:10]:
                item = product.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)

from .models import Purchase, Store, Vendor
from .forms import PurchaseForm, VendorForm, StoreForm

@login_required(login_url="/accounts/login/")
def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-date_added')
    return render(request, 'products/purchase_list.html', {'purchases': purchases})

@login_required(login_url="/accounts/login/")
def vendors_list(request):
    vendors = Vendor.objects.all().order_by('-date_added')
    return render(request, 'customers/vendors_list.html', {'vendors': vendors})

@login_required(login_url="/accounts/login/")
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:purchase_list')  # Make sure the redirect name matches the URL name
    else:
        form = PurchaseForm()
    return render(request, 'products/add_purchase.html', {'form': form, 'stores': Store.objects.all(), 'products': Product.objects.all(), 'vendors': Vendor.objects.all()})

def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:store_list')  # Adjust redirect URL as needed
    else:
        form = StoreForm()
    return render(request, 'products/add_store.html', {'form': form})

@login_required(login_url="/accounts/login/")
def store_list(request):
    stores = Store.objects.all().order_by('-date_added')  # Query for Store objects
    return render(request, 'products/store_list.html', {'stores': stores}) 

def store_inventory_view(request, store_id):
    # Get the store object based on store_id
    store = get_object_or_404(Store, pk=store_id)
    
    # Get inventory items for the store
    inventory_items = StoreInventory.objects.filter(store=store)
    
    context = {
        'store': store,
        'inventory_items': inventory_items,
    }
    return render(request, 'products/store_inventory.html', context)


def add_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:vendors_list')  # Adjust redirect URL as needed
    else:
        form = VendorForm()
    return render(request, 'products/add_vendor.html', {'form': form})

@login_required(login_url="/accounts/login/")
def product_reports(request):
    # Logic to generate product reports
    return render(request, 'products/reports.html')

@login_required(login_url="/accounts/login/")
def employee_reports(request):
    # Your logic to get employee report data
    return render(request, 'products/employee_reports.html')

@login_required(login_url="/accounts/login/")
def product_reports(request):
    # Your logic to get product report data
    return render(request, 'products/product_reports.html')

@login_required(login_url="/accounts/login/")
def reports(request):
    # Your logic to get product report data
    return render(request, 'products/reports.html')

@login_required(login_url="/accounts/login/")
def sales_reports(request):
    # Your logic to get stock report data
    return render(request, 'products/sales_reports.html')

@login_required(login_url="/accounts/login/")
def bp_vs_sl_reports(request):
    # Your logic to get BP vs SL report data
    return render(request, 'products/bp_vs_sl_reports.html')

@login_required(login_url="/accounts/login/")
def wastage_reports(request):
    # Your logic to get wastage report data
    return render(request, 'products/wastage_reports.html')
