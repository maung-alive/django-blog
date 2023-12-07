from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from .models import Article, Category, Comment

from blog.helpers import save_action
from django.utils import timezone

# Create your views here.
def home(request):
    if request.GET and request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    if request.GET.get('category'):
        category = get_object_or_404(Category, name=request.GET.get('category'))
        articles = Article.objects.filter(category=category).order_by('-pk')
    else:
        articles = Article.objects.all().order_by('-pk')
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        articles = articles.filter(title__contains=search).order_by('-pk')

    
    pinned = Article.objects.filter(pinned=True)
    paginator = Paginator(articles, 6).page(page)
    articles = paginator.object_list
    return render(request, 'core/index.html', { 'articles': articles, 'pinned': pinned, 'paginator': paginator })

def article(request, title):
    article = get_object_or_404(Article, title=title)
    related_articles = Article.objects.filter(author=article.author).order_by('?')[:3]
    return render(request, 'core/article.html', { 'article': article, 'related_articles': related_articles })

def comment(request, title):
    if request.POST and request.POST.get('text') and request.user.is_authenticated:
        article = get_object_or_404(Article, title=title)
        comment = Comment(article=article, text=request.POST.get('text'), user=request.user)
        comment.save()
        save_action(
                msg="Commented \"" + comment.text[:50] + "\" on " + article.title[:50],
                type="c",
                user=request.user
            )
        return redirect('web-article', title=title)
    else:
        return HttpResponseForbidden('<p class="text-xl">Only User can be comment</p>')
    
def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            save_action(
                msg="Login",
                type="i",
                user=request.user
            )
            return redirect('web-home')

    return render(request, 'core/login.html')
    
def logout_view(request):
    save_action(
        msg="Logout",
        type="i",
        user=request.user
    )
    logout(request)
    return render(request, 'core/logout.html')

def signup_view(request):
    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if pass1 == pass2:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_superuser=True,
                is_staff=True,
                username=username,
                password=pass1,
            )
            user = authenticate(request, username=username, password=pass1)
            if user is not None:
                login(request, user)
                return redirect('web-home')



    return render(request, 'core/signup.html')