from django.forms import TextInput, Select, FileInput, Textarea
from django import forms
from BD.models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category',  'title_image', 'text_image']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Заголовок',}),
            'text': Textarea(attrs={'class': 'form-control',
                                    'placeholder': 'Текст',}),
            'category': Select(attrs={'class': 'form-control',
                                      'placeholder': 'Категория',}),
            'title_image': FileInput(attrs={'class': 'form-control',
                                            'placeholder': 'Превью картинка',}),
            'text_image': FileInput(attrs={'class': 'form-control',
                                           'placeholder': 'Картинки'}),
        }

    def save(self, user, commit=True):
        post = super().save(commit=False)
        post.author = user
        if commit:
            post.save()
            self.save_m2m()
        return post


class ResponseForm(forms.Form):
    title = forms.CharField(label='Заголовок', max_length=100)
    text = forms.CharField(label='Текст')
    widgets = {
        'title': TextInput(attrs={'class': 'form-group', 'placeholder': 'Заголовок'}),
        'text': Textarea(attrs={'class': 'form-group', 'placeholder': 'Текст'}),
    }

class AcceptResponseForm(forms.Form):
    response_id = forms.IntegerField(widget=forms.HiddenInput())

class RejectResponseForm(forms.Form):
    response_id = forms.IntegerField(widget=forms.HiddenInput())