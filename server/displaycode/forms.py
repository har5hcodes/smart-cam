from django import forms
from .models import Comment, Snippet

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', 'line', 'snippetId',)

class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ('text',)
