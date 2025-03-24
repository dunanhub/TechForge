from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Product, Category, SubCategory
from .serializers import CategorySerializer, ProductSerializer

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {'categories': categories})

def subcategory_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category)
    return render(request, 'products/subcategory_by_category.html', {'subcategories': subcategories, 'category': category})

def product_list(request, category_id, subcategory_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(SubCategory, id=subcategory_id, category=category)
    products = Product.objects.filter(subcategory=subcategory)
    return render(request, 'products/products_by_category.html', {
        'category': category,
        'subcategory': subcategory,
        'products': products
    })

def product_detail(request, category_id, subcategory_id, product_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(SubCategory, id=subcategory_id, category=category)
    product = get_object_or_404(Product, id=product_id, subcategory=subcategory)

    return render(request, 'products/product_detail.html', {
        'category': category,
        'subcategory': subcategory,
        'product': product
    })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
