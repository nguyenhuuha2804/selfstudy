from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class CommentManager(models.Manager):
    def all(self):
        qs=super(CommentManager,self).filter(parent=None)
        return qs

    def filter_by_instance(self,instance):
        content_type=ContentType.objects.get_for_model(instance.__class__)
        object_id=instance.id
        qs=super(CommentManager,self).filter(content_type=content_type,object_id=object_id).filter(parent=None)
        return qs
        
class Comment(models.Model):
    #post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')

    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)

    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.member)
    def children(self): #replies
        return Comment.objects.filter(parent=self)
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
