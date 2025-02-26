from django.urls import resolve
from products.models import Category, SubCategory, Product

def breadcrumbs(request):
    path_parts = request.path.strip('/').split('/')
    breadcrumbs = []
    url_accum = ''

    for part in path_parts:
        url_accum += f'/{part}'
        name = part.replace('-', ' ').capitalize()  # Преобразуем URL в читаемый формат
        breadcrumbs.append({'name': name, 'url': url_accum})

    return {'breadcrumbs': breadcrumbs}
