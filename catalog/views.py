from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Product
from .forms import ProductForm, ProductModeratorForm

User = get_user_model()


class HomeListView(ListView):
    """Контроллер главной страницы - показывает только опубликованные продукты"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('name')


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер страницы товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = 'users:login'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания продукта - владелец назначается автоматически"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'

    def form_valid(self, form):
        """Автоматически назначаем владельца"""
        form.instance.owner = self.request.user
        form.instance.is_published = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер редактирования продукта - только владелец или модератор"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'

    def test_func(self):
        """Проверяем, может ли пользователь редактировать продукт"""
        product = self.get_object()
        user = self.request.user

        if product.owner == user:
            return True

        if user.has_perm('catalog.can_unpublish_product'):
            self.form_class = ProductModeratorForm
            return True

        return False

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления продукта - владелец или модератор"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    login_url = 'users:login'
    success_url = reverse_lazy('home')

    def test_func(self):
        """Проверяем, может ли пользователь удалить продукт"""
        product = self.get_object()
        user = self.request.user

        if product.owner == user:
            return True

        if user.has_perm('catalog.delete_product'):
            return True

        return False


class ProductModeratorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер для модерации продукта (только публикация)"""
    model = Product
    form_class = ProductModeratorForm
    template_name = 'catalog/product_moderate_form.html'
    login_url = 'users:login'

    def test_func(self):
        """Только модераторы могут модерировать"""
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def get_success_url(self):
        return reverse_lazy('home')


class ContactsTemplateView(TemplateView):
    """Контроллер страницы контактов"""
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение от {name} ({phone}): {message}')
        return self.render_to_response({})