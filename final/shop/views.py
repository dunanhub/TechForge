from django.shortcuts import render
from products.models import Product, Category, ProductImage

def homepage(request):
    return render(request, 'shop/index.html')

def products(request):
    product = Product.objects.all()
    return render(request, 'shop/products.html', {"products": product})

def categories_view(request):
    categories = [
        {"title": "Laptops", "description": "Find the latest high-performance laptops.", "image": "https://via.placeholder.com/200"},
        {"title": "PC Components", "description": "Upgrade your PC with top-quality components.", "image": "https://via.placeholder.com/200"},
        {"title": "Prebuilt Systems", "description": "Powerful prebuilt PCs ready to use.", "image": "https://via.placeholder.com/200"},
        {"title": "Accessories", "description": "Keyboards, mice, and other peripherals.", "image": "https://via.placeholder.com/200"},
        {"title": "Monitors", "description": "High-resolution monitors for gaming and work.", "image": "https://via.placeholder.com/200"},
        {"title": "Networking", "description": "Routers, switches, and network accessories.", "image": "https://via.placeholder.com/200"},
        {"title": "Storage", "description": "HDDs, SSDs, and external drives.", "image": "https://via.placeholder.com/200"},
        {"title": "Power Supplies", "description": "Reliable power solutions for your PC.", "image": "https://via.placeholder.com/200"},
    ]
    
    return render(request, 'shop/categories.html', {"categories": categories})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'shop/product_detail.html', {"product": product, "images": images})