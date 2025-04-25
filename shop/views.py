from django.shortcuts import render
from products.models import Product, Category, ProductImage
from django.core.paginator import Paginator

def homepage(request):
    category = Category.objects.all()
    return render(request, 'shop/index.html', {"categories": category})

def products(request):
    products = Product.objects.all()

    selected_categories = request.GET.getlist('category[]')
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    price_ranges = request.GET.getlist('price[]')
    if price_ranges:
        price_conditions = Q()
        for range in price_ranges:
            min_price, max_price = map(int, range.split('-'))
            price_conditions |= Q(price__gte=min_price, price__lte=max_price)
        products = products.filter(price_conditions)

    sort_option = request.GET.get('sort')
    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_params = request.GET.copy()
    if 'page' in current_params:
        del current_params['page']

    context = {
        'products': page_obj,
        'current_params': current_params.urlencode(),
        'categories': Category.objects.all(),
        'selected_categories': selected_categories,
        'selected_prices': price_ranges,
    }
    return render(request, 'shop/products.html', context)

def categories_view(request):
    category = Category.objects.all()
    return render(request, 'shop/categories.html', {"categories": category})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'shop/product_detail.html', {"product": product, "images": images})