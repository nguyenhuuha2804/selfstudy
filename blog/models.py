from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.urls import reverse
from comments.models import Comment
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from markdown2 import markdown

# Create your models here.
# models Tag
class Tag(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

# models Category
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_detail',args=[self.slug])
    def __str__(self):
        return self.name
    
# models Post
class Post(models.Model):
    STATUS_CHOICES=(
        ('Published','Published'),
        ('Draft','Draft'),
    )
    title = models.CharField(max_length=250)
    #body = models.TextField()
    body = RichTextUploadingField(blank=True, null = True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    tag = models.ManyToManyField(Tag,related_name='post_tags')
    seo_title = models.CharField(max_length=60,blank=True,null=True)
    seo_description = models.CharField(max_length=165,blank=True,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    author = models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    status = models.CharField(max_length=10,default='Draft',choices=STATUS_CHOICES)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField('Views', default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)   
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.slug])
    @property
    def comments(self):
        instance=self
        qs=Comment.objects.filter_by_instance(instance)
        return qs
    @property
    def get_content_type(self):
        instance=self
        content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_markdown(self):
        body = self.body
        markdown_text = markdown(body)
        return mark_safe(markdown_text)