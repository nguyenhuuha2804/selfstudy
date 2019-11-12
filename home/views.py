from django.shortcuts import render
from blog.models import Post, Category
from django.db.models import Count
from django.db.models import Max
# Create your views here.
def contact(request):
    template = 'pages/contact.html'

    # import sliderbar of data
    category=Category.objects.annotate(posts_count = Count('post'))
    category_count =round(Category.objects.count()/2)
    posts= Post.objects.all()
    max_view = posts.aggregate(Max('views'))
    post = Post.objects.filter(status='Published').order_by("-published")[:5]
    post_new = Post.objects.filter(status='Published').order_by("-published")[:5]
    context={
        'category':category,
        'category_count':category_count,
        'post':post,
        'max_view':max_view,
        'post_new':post_new
    }
    return render(request,template,context)

def error404(request,exception):
    return render(request,'pages/error.html')
    
def error500(request):
    return render(request,'pages/error.html')