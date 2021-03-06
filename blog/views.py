from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import AddPostForm, UpdatePostForm, AddCommentForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer
from hitcount.views import HitCountDetailView
from django.http import JsonResponse
from django.core import serializers

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    paginate_by = 1
    
    def get_context_data(self, **kwargs):
        posts = Post.objects.order_by('-post_date')
        featured = posts.filter(featured=True).order_by('-post_date')[:2]
        featured_categories = posts.filter(featured=True).order_by('-post_date')[:3]
        popular = posts.order_by('-views')[:6]
        recent = posts[:4]

        class category:
            def __init__(self, name, count):
                self.name = name
                self.count = count

            
        articles = category('مقالات',10)
        news = category('أخبار',20)
        tutorials = category('دروس',30)

        
        context = super().get_context_data(**kwargs)
        context = {
            'recent' : recent,
            'featured': featured,
            'popular': popular,
            'featured_categories': featured_categories,
            'categories': [articles, news, tutorials],
        }

        return context


class CategoryView(ListView):
    model = Post
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(category__slug=self.kwargs["category_slug"]).order_by('-post_date')
        category =  Category.objects.get(slug=self.kwargs["category_slug"])
        featured = posts.filter(featured=True)[:3]
        recent = posts[:4]
        popular = posts.order_by('-views')[:6]

        context = super().get_context_data(**kwargs)
        context = {
            'category': category,
            'posts' : posts,
            'featured': featured,
            'recent' : recent,
            'popular': popular,
        }

        return context


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'post_detail.html'
    form = AddCommentForm
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form"] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(request.META['HTTP_REFERER'])


class AddPostView(CreateView):
    model = Post
    form_class = AddPostForm
    template_name = 'add_post.html'

    # gets the user id
    def form_valid(self, form):
        print(form)
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'update_post.html'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


def LoadMore(request):
    offset = int(request.POST['offset'])
    limit = 2
    posts = Post.objects.order_by('-post_date')[offset:limit+offset]
    totalData = Post.objects.count()
    data = {}
    posts__json = serializers.serialize('json',posts)
    return JsonResponse(data={
        'posts':posts__json,
        'totalResult':totalData
    })

def SearchPosts(request):
    if request.method == "POST":
        searched = request.POST['search']
        posts = Post.objects.filter(title__contains=searched)

        return render(request, 
            'search_posts.html',
            {'searched':searched,
            'posts':posts})
    else:
        return render(request, 
        'search_posts.html',
        {})
