from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="web-dashboard"),
    path('articles/', views.articles, name="dashboard-articles"),
    path('categories/', views.categories, name="dashboard-categories"),
    path('new/articles/', views.new_articles, name="dashboard-new-articles"),
    path('articles/<str:title>/', views.article_detail, name="dashboard-article"),
    path('settings/', views.settings, name="dashboard-settings"),
    path('delete/comment', views.delete_comment, name="delete-comment"),
    path('delete/article', views.delete_article, name="delete-article"),
    path('delete/account', views.delete_account, name="delete-account")
]