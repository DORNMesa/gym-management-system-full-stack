from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, ProductCategory
from datetime import datetime
from transaction.models import Credit
from user.models import MetaData
from decimal import Decimal
import os
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch

@cache_page(60 * 15)  # Cache for 15 minutes
def index(request):
    """
    Display and handle product management operations.
    """
    page_number = request.GET.get('page', 1)
    products = Product.objects.select_related('category').order_by("-id")
    paginator = Paginator(products, 10)  # 10 items per page
    page_obj = paginator.get_page(page_number)
    
    categories = ProductCategory.objects.all()

    if request.method == "POST":
        try:
            product_data = {
                'name': request.POST.get("name"),
                'category_id': request.POST.get("category"),
                'price': request.POST.get("price"),
                'stock': request.POST.get("stock"),
                'description': request.POST.get("description"),
                'image': request.FILES.get("image")
            }
            
            Product.objects.create(**product_data)
            messages.success(request, "Product added successfully")
            return redirect("/product/")
        except Exception as e:
            messages.error(request, f"Failed to add product: {str(e)}")
            return redirect("/product/")

    context = {
        'products': page_obj,
        'categories': categories
    }
    return render(request, 'product/index.html', context)

def sell(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        
        product = Product.objects.get(id=product_id)
        
        if product.stock < quantity:
            messages.error(request, "Insufficient stock")
            return redirect("/product/")
            
        # Convert to Decimal for consistent decimal arithmetic
        total_price = float(product.price * quantity)
        timestamp = int(datetime.now().timestamp())
        
        # Update stock
        product.stock -= quantity
        product.save()
        
        # Create transaction
        Credit.objects.create(
            trxId='FK-TRX-' + str(timestamp),
            reason='product_sale',
            amount=total_price,
            date=datetime.now()
        )
        
        # Update funds - convert to float since MetaData uses FloatField
        meta = MetaData.objects.last()
        meta.funds = float(meta.funds) - total_price
        meta.save()
        
        messages.success(request, "Product sold successfully")
        return redirect("/product/")  # Added return statement
# Create your views here.

def edit(request, pk):
    product = get_object_or_404(Product, id=pk)
    categories = ProductCategory.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        description = request.POST.get("description")
        is_available = request.POST.get("is_available") == "on"
        new_image = request.FILES.get("image")

        # Handle image update
        if new_image:
            # Delete old image if it exists
            if product.image:
                if os.path.isfile(product.image.path):
                    os.remove(product.image.path)
            product.image = new_image

        product.name = name
        product.category_id = category_id
        product.price = price
        product.stock = stock
        product.description = description
        product.is_available = is_available
        product.save()

        messages.success(request, "Product updated successfully")
        return redirect("/product/")

    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'product/edit.html', context)

def delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    # Delete the image file if it exists
    if product.image:
        if os.path.isfile(product.image.path):
            os.remove(product.image.path)
    product.delete()
    messages.success(request, "Product deleted successfully")
    return redirect("/product/")
