from django import forms
from .models import ArticlePost

class ArticlePostForm(forms.ModelForm):
    # internal class
    class Meta:
        # specify the origin model
        model = ArticlePost
        # define the fields of the forms
        fields = ('title', 'body')

