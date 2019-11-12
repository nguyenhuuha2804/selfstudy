from django.urls import path, include

from .views import post_list, post_detail,category_detail,search,new_post, \
    post_list_admin, edit_post, delete_post, new_category,list_category,main

urlpatterns=[
    path('results/',search,name='search'),
    path('post-detail/<slug:slug>/',post_detail,name='post_detail'),
    path('category-detail/<slug:slug>/',category_detail,name='category_detail'),
    #custom admin
    path('new-post/',new_post,name='new_post'),
    path('post-list/',post_list_admin,name='post_list_admin'),
    path('edit-post/<int:pk>/',edit_post,name='edit_post'),
    path('delete-post/<int:pk>/',delete_post,name='delete_post'),
    path('dashboard/',main,name='dashboard'),
    path('list-category/',list_category,name='list_category'),
    path('new-category/',new_category,name='new_category'),
]