from django.views.generic import ListView, DetailView, TemplateView
from .models import Product


class HomeListView(ListView):
    """Контроллер главной страницы с выводом всех продуктов"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Контроллер страницы товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsTemplateView(TemplateView):
    """Контроллер страницы контактов"""
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение от {name} ({phone}): {message}')
        return self.render_to_response({})