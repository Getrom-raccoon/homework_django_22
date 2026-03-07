from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost


class BlogPostListView(ListView):
    """Список всех опубликованных статей"""
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Выводим только опубликованные статьи"""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная страница статьи"""
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при открытии статьи"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    """Создание новой статьи"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:blogpost_list')


class BlogPostUpdateView(UpdateView):
    """Редактирование статьи"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        """После успешного редактирования перенаправляем на страницу статьи"""
        return reverse_lazy('blog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление статьи"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')