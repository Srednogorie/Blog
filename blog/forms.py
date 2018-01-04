from django import forms
from .models import Comment
from .models import Email


class EmailPostForm(forms.Form):
    name = forms.CharField(label='Test label', required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Name *'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'E-mail *'}))
    company = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Company'}))
    comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Your comment hire *'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')


class EmailSign(forms.ModelForm):
    email = forms.EmailField(label='', required=True,
                             widget=forms.EmailInput(attrs={'type': 'text', 'value': "Enter your e-mail here",
                                                            'onfocus': "this.value = ''",
                                                            'onblur': "if (this.value == '') {this.value = 'Enter your e-mail here'}",
                                                            'id': "sign_email"}))

    class Meta:
        model = Email
        fields = ('email',)


class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'type': 'text', 'class': 'text-box',
                                                                    'placeholder': 'Search for blog'}))