from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Product
from .forms import ProductForm


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


class ProductCreateView(CreateView):
    """Контроллер создания продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')


class ProductUpdateView(UpdateView):
    """Контроллер редактирования продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    """Контроллер удаления продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')


class ContactsTemplateView(TemplateView):
    """Контроллер страницы контактов"""
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение от {name} ({phone}): {message}')
        return self.render_to_response({})