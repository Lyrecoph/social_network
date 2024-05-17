from django import forms
# from django.forms.widgets import ClearableFileInput

from social.models import Post, Media

# Génère le formulaire pour créer un post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
        

# class CustomClearableFileInput(ClearableFileInput):
#     def __init__(self, attrs=None):
#         super().__init__(attrs)
#         if attrs is None:
#             attrs = {}
#         attrs.update({'multiple': True})
#         self.attrs = attrs
        
# Génère le formulaire pour ajouter une image
# class MediaForm(forms.Form):
#     images = forms.FileField(widget=CustomClearableFileInput(), required=False)
    
class MediaForm(forms.ModelForm):
    
    class Meta:
        model = Media
        fields = ('image',)
#         widgets = {
#             'image': forms.ClearableFileInput(attrs={'multiple': True}),
#         }
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].required = False
        