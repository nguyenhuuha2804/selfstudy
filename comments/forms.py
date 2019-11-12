from django import forms

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    body = forms.CharField(label='',widget=forms.Textarea(attrs={'rows':1, 'cols':5}))