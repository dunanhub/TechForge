from django.shortcuts import render, redirect, get_object_or_404
from products.models import Category, Product
from .forms import CategoryForm, ProductForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'adminpanel/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:category_list')
    else:
        form = CategoryForm()
    return render(request, 'adminpanel/add_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'adminpanel/edit_category.html', {'form': form, 'category': category})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('adminpanel:category_list')
    return render(request, 'adminpanel/delete_category.html', {'category': category})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:product_list')
    else:
        form = ProductForm()
    return render(request, 'adminpanel/add_product.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'adminpanel/edit_product.html', {'form': form, 'product': product})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('adminpanel:product_list')
    return render(request, 'adminpanel/delete_product.html', {'product': product})