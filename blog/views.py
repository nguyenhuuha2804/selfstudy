from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Post, Category, Tag
from comments.models import Comment
from comments.forms import CommentForm
from .forms import PostForm, CategoryForm
from selfstudy.config import pagination, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.db.models import Count
from django.db.models import Max
# Create your views here.

def post_list(request):
    template='pages/home.html'
    object_list=Post.objects.filter(status='Published').exclude(category__slug = 'giai-tri').order_by("-published")
    pages=pagination(request,object_list,5)
    
    # import sliderbar of data
    category=Category.objects.annotate(posts_count = Count('post'))
    category_count =round(Category.objects.count()/2)
    posts= Post.objects.all()
    max_view = posts.aggregate(Max('views'))
    post = Post.objects.filter(status='Published').order_by("-published")[:5]
    post_new = Post.objects.filter(status='Published').order_by("-published")[:5]
    context={
        'items':pages[0],
        'page_range':pages[1],
        'post':post,
        'category':category,
        'category_count':category_count,
        'max_view':max_view,
        'post_new':post_new
    }
    return render(request,template,context)

def post_detail(request,slug):
    template='blog/post_detail.html'
    
    post1=get_object_or_404(Post,slug=slug)
    tag=post1.tag.all()
    post2 = Post.objects.filter(category = post1.category).order_by("-published")[0:3]

    # import sliderbar of data
    category=Category.objects.annotate(posts_count = Count('post'))
    category_count =round(Category.objects.count()/2)
    posts= Post.objects.all()
    max_view = posts.aggregate(Max('views'))
    post = Post.objects.filter(status='Published').order_by("-published")[:5]
    post_new = Post.objects.filter(status='Published').order_by("-published")[:5]
    if request.user.is_authenticated:
        Post.viewed(self=post1)

    views = post1.views
    initial_data = {
            'content_type':post1.get_content_type,
            'object_id':post1.id
    }
    form = CommentForm(request.POST or None,initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model = c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('body')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                        member = request.user,
                        content_type = content_type,
                        object_id = obj_id,
                        body = content_data,
                        parent = parent_obj,
                )
        return HttpResponseRedirect(new_comment.content_object.get_absoulte_url())

    comments = post1.comments
    post = Post.objects.filter(status='Published').order_by("-published")[0:5]

    context={
        'post1':post1,
        'post2':post2,
        'comments':comments,
        'comment_form':form,
        'post':post,
        'tag':tag,
        'views':views,
        'post':post,
        'category':category,
        'category_count':category_count,
        'max_view':max_view,
        'post_new':post_new,
        }
    return render(request,template,context)

def category_detail(request,slug):
    template = 'blog/category_detail.html'
    Post1 = Post.objects.filter(status='Published')

    # import sliderbar of data
    category=Category.objects.annotate(posts_count = Count('post'))
    category_count =round(Category.objects.count()/2)
    posts= Post.objects.all()
    max_view = posts.aggregate(Max('views'))
    post = Post.objects.filter(status='Published').order_by("-published")[:5]
    post_new = Post.objects.filter(status='Published').order_by("-published")[:5]
    if slug:
        category_slug = get_object_or_404(Category,slug = slug)
        Post1 = Post1.filter(category = category_slug)
    context={
        'category1':category_slug,
        'Post1':Post1,
        'post':post,
        'category':category,
        'category_count':category_count,
        'max_view':max_view,
        'post_new':post_new
    }
    return render(request,template,context)


def search(request):
    template='blog/result_search.html'

    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(Q(title__icontains = query) | Q(body__icontains = query))
    else:
        results = Post.objects.filter(status = "Published")

    pages = pagination(request,results,num = 2)

    # import sliderbar of data
    category=Category.objects.annotate(posts_count = Count('post'))
    category_count =round(Category.objects.count()/2)
    posts= Post.objects.all()
    max_view = posts.aggregate(Max('views'))
    post = Post.objects.filter(status='Published').order_by("-published")[:5]

    context = {
        'results':results,
        'items':pages[0],
        'page_range':pages[1],
        'query':query,
        'post':post,
        'category':category,
        'category_count':category_count,
        'max_view':max_view
    }
    return render(request,template,context)

def new_post(request):
    template = 'backend/new_post.html'
    form = PostForm(request.POST or None)
    try:
        if form.is_valid():
            form.save()
            messages.success(request,'Blog post was saved to the database')
    except Exception as e:
        form = PostForm()
        messages.warning(request,'Blog was not saved.Error {}'.format(e))

    context = {
        'form':form,
    }
    return render(request,template,context)

def edit_post(request,pk):
    template = 'backend/new_post.html'
    post = get_object_or_404(Post,pk = pk)

    if request.method == "POST":
        form = PostForm(request.POST,instance = post)
        try:
            if form.is_valid():
                form.save()
                messages.success(request,'Your Blog post has been Updated')
        except Exception as e:
            messages.warning(request,'Your post was not saved do to an error: {}'.format(e))
    else:
        form = PostForm(instance = post)
    context = {
        'form':form,
        'post':post,
    }
    return render(request,template,context)

def delete_post(request,pk):
    template = 'backend/new_post.html'
    post = get_object_or_404(Post,pk = pk)
    try:
        if request.method == 'POST':
            form = PostForm(request.POST,instance = post)
            post.delete()
            messages.success(request,'You have successfully delete the post')
        else:
            form = PostForm(instance = post)
    except Exception as e:
        messages.warning(request,'The post could not be delete: Error {}'.format(e))
    context={
        'form':form,
        'post':post,
    }
    return render(request,template,context)

def post_list_admin(request):
    template = 'backend/post_list_admin.html'
    post = Post.objects.all()
    pages = pagination(request,post,5)

    context={
        'items':pages[0],
        'page_range':pages[1],
    }
    return render(request,template,context)
def list_category(request):
    template = 'backend/list_category.html'
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request,template,context)
def main(request):
    template = 'backend/main.html'
    context ={}
    return render(request,template,context)
def new_category(request):
    template = 'backend/new_category.html'
    form = CategoryForm(request.POST or None)
    try:
        if form.is_valid():
            form.save()
            messages.success(request,'Blog category was saved to the database')
    except Exception as e:
        form = PostForm()
        messages.warning(request,'Blog category was not saved.Error {}'.format(e))

    context = {
        'form':form,
    }
    return render(request,template,context)
