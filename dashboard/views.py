from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from core.models import Article, Comment, Category
from django.contrib.auth.models import User
from dashboard.models import Action

from blog.helpers import save_action

# Create your views here.
def home(request):
    articles_count = Article.objects.all().order_by('-pk').count()
    users_count = User.objects.all().order_by('-pk').count()
    comments_count = Comment.objects.all().order_by('-pk').count()
    category_count = Category.objects.all().order_by('-pk').count()
    actions = Action.objects.filter(user=request.user.pk).order_by('-pk')[:10]
    return render(request, 'dashboard/home.html', {
        "actions": actions,
        "articles_count": articles_count,
        "users_count": users_count,
        "comments_count": comments_count,
        "category_count": category_count,
    })

def articles(request):
    articles = Article.objects.filter(author=request.user.pk).order_by('-pk')

    return render(request, 'dashboard/articles.html', {
        "articles": articles,
    })

def new_articles(request):
    if request.POST and request.POST.get('submit') == 'create':
        title = request.POST.get('title')
        content = request.POST.get('text')
        cover = request.FILES.get('cover')
        article = Article(
            title=title,
            category=None,
            content=content,
            cover=cover,
        )
        article.author = request.user
        article.save()
        save_action(
            msg="Create article " + title[:50],
            type="c",
            user=request.user
        )
        messages.success(request, f"{title[:50]} was created")
        return redirect('web-dashboard')
    
    categories = Category.objects.all().order_by('-pk')
    
    return render(request, 'dashboard/new_articles.html', { 'categories': categories })

def article_detail(request, title):
    article = get_object_or_404(Article, title=title)
    categories = Category.objects.all().order_by('-pk')

    if request.POST and request.POST.get('submit') == 'update' and article.author == request.user.pk:
        article_title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('text')
        cover = request.FILES.get('cover')
        article.title = article_title
        article.category = Category.objects.get(name=category) if category != 'None' else None
        article.content = content
        article.cover = cover
        article.save()
        save_action(
            msg="Update the " + article.title[:50],
            type="u",
            user=request.user
        )
        return redirect('web-article', title=title)

    return render(request, 'dashboard/article_detail.html', { 'article': article, 'categories': categories })

def categories(request):
    cats = Category.objects.all().order_by('-pk')
    pinned = Article.objects.filter(pinned=True).order_by('-pk')
    articles = Article.objects.filter(author=request.user.pk).order_by('-pk')

    if request.GET and request.GET.get('type') == "remove" and request.GET.get('title'):
        article = Article.objects.get(title=request.GET.get('title'))
        if request.GET.get('cat') == 'pin' and article.author == request.user:
            article.pinned = False
            article.save()
            save_action(
                msg="Unpinned the " + article.title[:50],
                type="u",
                user=request.user
            )
            messages.success(request, f"{article.title[:50]} is removed from pins")

        elif request.GET.get('cat') != 'pin' and article.author == request.user:
            article.category = None
            article.save()
            save_action(
                msg="Uncategorized the " + article.title[:50],
                type="u",
                user=request.user
            )
            messages.success(request, f"{article.title[:50]} is uncategorized!")

        else:
            pass

    elif request.GET and request.GET.get('type') == "add" and request.GET.get('title') != None:
        article = Article.objects.get(title=request.GET.get('title'))
        if request.GET.get('cat') == 'Pinned' and article.author == request.user:
            article.pinned = True
            article.save()
            save_action(
                msg="Pinned the " + article.title[:50],
                type="u",
                user=request.user
            )
        elif request.GET.get('cat') != 'Pinned' and article.author == request.user:
            article.category = Category.objects.get(name=request.GET.get('cat'))
            article.save()
            save_action(
                msg="Categorized the " + article.title[:50],
                type="u",
                user=request.user
            )
        else:
            pass
    elif request.GET and request.GET.get('type') == "add" and request.GET.get('title') == None:
        category = Category.objects.create(name=request.GET.get('cat'))
        messages.success(request, f"category {category.name[:50]} is created!")


    return render(request, 'dashboard/categories.html', { "articles": articles, "cats": cats, 'pinned': pinned})

def settings(request):
    submit_type = request.POST.get('submit')
    if request.POST and submit_type == 'cgpw':
        if request.POST.get('pass1') == request.POST.get('pass2'):
            user = User.objects.get(username=request.user.username)
            user.set_password(raw_password=request.POST.get('pass1'))
            user.save()
            save_action(
                msg="Change password",
                user=request.user,
                type="i"
            )
            messages.success(request, f"Password changed!")


    elif request.POST and submit_type == 'svinfo':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        user = User.objects.get(username=request.user.username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        save_action(
            msg="Change profile information",
            type="i",
            user=request.user
        )
        messages.success(request, f"You've changed your profile info")


    return render(request, 'dashboard/settings.html', {
        
    })

def delete_comment(request):
    if request.GET and request.GET.get('pk'):
        comments = Comment.objects.filter(pk=request.GET.get('pk')) if request.GET.get('pk') != 'all' else Comment.objects.all()
        for comment in comments:
            save_action(
                msg="Deleted comment \"" + comment.text[:50] + "\" on " + comment.article.title[:50],
                type="d",
                user=request.user
            )
            comment.delete()
            
        return redirect('dashboard-settings')

def delete_article(request):
    if request.GET and request.GET.get('pk'):
        articles = Article.objects.filter(pk=request.GET.get('pk')) if request.GET.get('pk') != 'all' else Article.objects.all()
        for article in articles:
            save_action(
                msg="Delete article: " + article.title[:50],
                type="d",
                user=request.user
            )
            article.delete()

        return redirect('dashboard-settings')
    
def delete_account(request):
    if request.GET and request.GET.get('username') == request.user.username:
        User.objects.get(username=request.GET.get('username')).delete()
        return redirect('web-login')