from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from .forms import ProductForm, ProductModeratorForm
from .models import Category, Product
from .services import get_products_by_category

User = get_user_model()


def category_products_view(request, category_id):
    """
    Представление для отображения всех продуктов в указанной категории
    """
    category = get_object_or_404(Category, pk=category_id)

    products = get_products_by_category(category_id)

    context = {
        'category': category,
        'products': products,
        'products_count': len(products) if products else 0,
    }

    return render(request, 'catalog/category_products.html', context)


class HomeListView(ListView):
    """Контроллер главной страницы - показывает только опубликованные продукты"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер страницы товара с кешированием"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = 'users:login'

    def get_object(self, queryset=None):
        """Получаем объект с кешированием"""
        pk = self.kwargs.get('pk')

        cache_key = f'product_{pk}'
        product = cache.get(cache_key)

        if not product:
            product = super().get_object(queryset)
            cache.set(cache_key, product, timeout=300)
            print(f'Данные продукта {pk} загружены из БД и сохранены в кеш')
        else:
            print(f'Данные продукта {pk} загружены из кеша Redis')

        product.views_count += 1
        product.save()

        return product


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

