"""
Ali Abdulmadzhidov 21.03.17
"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
