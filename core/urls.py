from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="web-home"),
    path('articles/<str:title>', views.article, name="web-article"),
    path('articles/<str:title>/comment', views.comment, name="web-comment"),
    path('logout', views.logout_view, name="web-logout"),
    path('login', views.login_view, name="web-login"),
    path('sign-up', views.signup_view, name="web-signup")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)