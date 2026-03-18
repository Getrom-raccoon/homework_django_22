from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Product
from .forms import ProductForm


class HomeListView(ListView):
    """Контроллер главной страницы с выводом всех продуктов (общедоступный)"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('name')


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер страницы товара (только для авторизованных)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = 'users:login'  # Перенаправление на страницу входа


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления продукта (только для авторизованных)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'users:login'


class ContactsTemplateView(TemplateView):
    """Контроллер страницы контактов (общедоступный)"""
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение от {name} ({phone}): {message}')
        return self.render_to_response({})