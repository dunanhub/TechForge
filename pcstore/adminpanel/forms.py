from django import forms
from django.forms import inlineformset_factory
from products.models import Category, SubCategory, Product, ProductImage
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    """ Форма для добавления категории """
    class Meta:
        model = Category
        fields = ['name', 'image']

class SubCategoryForm(forms.ModelForm):
    """ Форма для добавления подкатегории """
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'image']

    def clean_name(self):
        """ Проверка на уникальность подкатегории в рамках одной категории """
        name = self.cleaned_data['name']
        category = self.cleaned_data['category']
        if SubCategory.objects.filter(name=name, category=category).exists():
            raise ValidationError('Подкатегория с таким именем уже существует в данной категории.')
        return name

class ProductForm(forms.ModelForm):
    """ Форма для добавления товара """
    class Meta:
        model = Product
        fields = ['subcategory', 'name', 'description', 'price', 'stock', 'specifications']

class ProductImageForm(forms.ModelForm):
    """ Форма для добавления изображений товаров """
    class Meta:
        model = ProductImage
        fields = ['image']

# Inline Formset для загрузки нескольких изображений для товара
ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=3, can_delete=True
)
