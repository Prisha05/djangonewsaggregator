from django.shortcuts import render, redirect
from django.contrib import messages
from .models import News, Category, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def home(request):
    first_news = News.objects.first()
    three_news = News.objects.all()[1:3]
    three_categories = Category.objects.all()[0:3]
    return render(request, 'home.html', {
        'first_news': first_news,
        'three_news': three_news,
        'three_categories': three_categories
    })

def all_news(request):
    all_news = News.objects.all()
    return render(request, 'all-news.html', {
        'all_news': all_news
    })

def detail(request, id):
    news = News.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        comment_text = request.POST['message']

        Comment.objects.create(
            news=news,
            name=name,
            email=email,
            comment=comment_text,
            status=False  # Assuming you want to moderate comments before displaying them
        )

        messages.success(request, 'Comment submitted but in moderation mode.')

    category = Category.objects.get(id=news.category.id)
    rel_news = News.objects.filter(category=category).exclude(id=id)
    comments = Comment.objects.filter(news=news, status=True).order_by('-id')

    return render(request, 'detail.html', {
        'news': news,
        'related_news': rel_news,
        'comments': comments
    })

def all_category(request):
    cats = Category.objects.all()
    return render(request, 'category.html', {
        'cats': cats
    })

def category(request, id):
    category = Category.objects.get(id=id)
    news = News.objects.filter(category=category)
    return render(request, 'category-news.html', {
        'all_news': news,
        'category': category
    })

@login_required
def like_news(request, id):
    if request.method == 'POST':
        news = get_object_or_404(News, pk=id)
        if request.user in news.liked_by.all():
            news.liked_by.remove(request.user)
        else:
            news.liked_by.add(request.user)
        return JsonResponse({'likes': news.liked_by.count()})
    else:
        return JsonResponse({})

@login_required
def share_news(request, id):
    if request.method == 'POST':
        news = get_object_or_404(News, pk=id)
        if request.user in news.shared_by.all():
            news.shared_by.remove(request.user)
        else:
            news.shared_by.add(request.user)
        return JsonResponse({'shares': news.shared_by.count()})
    else:
        return JsonResponse({})

@login_required
def add_comment(request, id):
    if request.method == 'POST':
        news = get_object_or_404(News, pk=id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('message')

        Comment.objects.create(
            news=news,
            name=name,
            email=email,
            comment=comment_text,
            status=True  # Assuming you want to display the comments immediately
        )

        messages.success(request, 'Comment submitted successfully.')

        return redirect('detail', id=id)
    else:
        return JsonResponse({'success': False})
