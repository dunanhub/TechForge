from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from products.models import Category, Product, ProductImage, SubCategory
from .forms import CategoryForm, ProductForm, ProductImageForm, SubCategoryForm

ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=4, can_delete=True)


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



def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category)
    return render(request, 'adminpanel/subcategory_list.html', {'category': category, 'subcategories': subcategories})

def add_subcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            return redirect('adminpanel:subcategory_list', category_id=category_id)
    else:
        form = SubCategoryForm()
    return render(request, 'adminpanel/add_subcategory.html', {'form': form, 'category': category})

def edit_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:subcategory_list', category_id=subcategory.category.id)
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, 'adminpanel/edit_subcategory.html', {'form': form, 'subcategory': subcategory})

def delete_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    category_id = subcategory.category.id
    if request.method == 'POST':
        subcategory.delete()
        return redirect('adminpanel:subcategory_list', category_id=category_id)
    return render(request, 'adminpanel/delete_subcategory.html', {'subcategory': subcategory})




def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save()
            formset.instance = product
            formset.save()
            return redirect('adminpanel:product_list')
    else:
        product_form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, 'adminpanel/add_product.html', {
        'product_form': product_form,
        'formset': formset
    })

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('adminpanel:product_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, 'adminpanel/edit_product.html', {
        'form': form,
        'formset': formset,
        'product': product,
    })

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('adminpanel:product_list')
    return render(request, 'adminpanel/delete_product.html', {'product': product})
