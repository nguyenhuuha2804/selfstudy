from django.shortcuts import render, redirect
from blog.models import Post, Category
from django.db.models import Count
from django.db.models import Max
from django.core.mail import send_mail
from selfstudy.settings import EMAIL_HOST_USER
from django.contrib import messages
import re, sys

TAG_RE = re.compile(r'<[^>]+>')

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
    
    if request.method == 'POST':
        email = request.POST['email']
        noidung = request.POST['noidung']
        subject = 'Hãy hỗ trợ tôi theo địa chỉ email:  ' + str(email)
        
        message = remove_tags(str(noidung))

        send_mail(subject, 
            message, EMAIL_HOST_USER, ['huuha84@gmail.com'], fail_silently = False)
        messages.info(request,'Liên hệ đã gửi thành công!')
        return redirect('contact')
        
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

def remove_tags(text):
    return TAG_RE.sub('', text)