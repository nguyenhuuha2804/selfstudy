from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display=['id','name']
admin.site.register(Tag,TagAdmin)
class PostAdmin(admin.ModelAdmin):
    exclude=('slug',)
    list_display=['title','category','author','published']
    list_filter=['published']
    search_fields=['id']
admin.site.register(Post,PostAdmin)
class CategoryAdmin(admin.ModelAdmin):
    exclude=('slug',)
    list_display=['id','name','slug']
admin.site.register(Category,CategoryAdmin)