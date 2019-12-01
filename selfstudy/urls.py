"""selfstudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from home import views
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from account.views import (login_view,register_view,logout_view)
from blog.views import post_list
from django.views.generic import TemplateView
from django.conf.urls import url
from home.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',post_list,name='home'),
    path('contact/',views.contact,name='contact'),
    path('blog/',include(('blog.urls','blog'),namespace='blog')),
    path('login/', login_view, name='login'),
    path('logout/',logout_view,name='logout'),
    path('register/',register_view,name='register'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('robots.txt', TemplateView.as_view(template_name="pages/robots.txt", content_type='text/plain')),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps}),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    
handler404 = 'home.views.error404'
handler500 = 'home.views.error500'