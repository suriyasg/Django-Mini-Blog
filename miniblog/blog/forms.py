from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


import datetime


class CommentForm(forms.Form):
    content = forms.CharField(
            label="Your Comment",
            widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            required=True,
            initial="write your comment"
        )
    
    def clean_content(self):
        data = self.cleaned_data['content']

        if len(data) < 3:
            raise ValidationError(_('Invalid comment - Too Short!'))
        if (len(data) > 1000):    
            raise ValidationError(_('Invalid comment - Too Long!'))
        
        return data
