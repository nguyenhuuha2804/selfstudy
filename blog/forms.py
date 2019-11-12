from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','body','category','seo_title','seo_description','status']
        widgets={
            'title':forms.TextInput(attrs={'rows':1, 'cols':40}),
            
            'category':forms.Select(attrs={'rows':1, 'cols':15}),
            'seo_title':forms.TextInput(attrs={'class':'form-control'}),
            'seo_description':forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'rows':1, 'cols':8}),
        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
        }