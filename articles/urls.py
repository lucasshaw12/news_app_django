# articles/urls.py
from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, ArticleCreateView, SearchResultsView, TagListView

urlpatterns = [
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("<int:pk>", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("new/", ArticleCreateView.as_view(), name="article_new"),
    path("", ArticleListView.as_view(), name="article_list"),
    path("tags/<slug:tag_slug>/", TagListView.as_view(), name="article_list"),
]