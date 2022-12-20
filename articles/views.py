from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .models import Article
from .forms import CommentForm


# Create your views here.
class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Article.tags.most_common()[:10]
        return context


class ArticleListView(LoginRequiredMixin, TagMixin, ListView):
    model = Article
    template_name = "article_list.html"


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_new.html"
    fields = (
        "title",
        "body",
        "tags",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TagListView(TagMixin, ListView):
    model = Article
    template_name = "article_list.html"
    common_tags = Article.tags.most_common()[:4]

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get('tag_slug'))


class CommentGet(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = self.get_object()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = (
        "title",
        "body",
        "tags",
    )
    template_name = "article_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user, self.request.user.is_superuser


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class SearchResultsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Article.objects.filter(
            Q(title__icontains=query) | Q(date__icontains=query) | Q(author__username__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class MyPostsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "my_posts.html"

    def get_queryset(self):
        query = Article.objects.all()
        object_list = query.filter(author=self.request.user)
        return object_list

class MyTodoApp(LoginRequiredMixin):
    ...