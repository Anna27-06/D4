from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostFormNews, PostFormArticle
from django.urls import reverse, reverse_lazy



class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context


class PostSearch(PostsList):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context


class PostCreateNews(CreateView):
    form_class = PostFormNews
    model = Post
    template_name = 'post_createnews.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts_detail', kwargs={'pk': self.object.id})


class PostCreateArticle(CreateView):
    form_class = PostFormArticle
    model = Post
    template_name = 'post_createarticle.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles_detail', kwargs={'pk': self.object.id})


class PostsUpdateNews(UpdateView):
    form_class = PostFormNews
    model = Post
    template_name = 'post_createnews.html'


class PostsUpdateArticles(UpdateView):
    form_class = PostFormArticle
    model = Post
    template_name = 'post_createarticle.html'


class PostsDeleteNews(DeleteView):
    model = Post
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('posts_list')


class PostsDeleteArticles(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts_list')