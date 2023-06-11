from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    required_css_class = 'my-custom-class'
    title = forms.CharField(max_length=40)

    class Meta:
       model = Post
       fields = [
           'posttitle',
           'postauthor',
           'postnewstype',
           'postcat',
           'posttext',
       ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})
        self.fields['posttitle'].label = "Заголовок публикации"
        self.fields['posttitle'].widget.attrs.update({'placeholder': "Введите название"})
        self.fields['posttext'].label = "Текст публикации"
        self.fields['posttext'].widget.attrs.update({'placeholder': "Введите текст здесь"})

    def clean(self):
       cleaned_data = super().clean()
       posttitle = cleaned_data.get("posttitle")
       posttext = cleaned_data.get("posttext")

       if posttitle == posttext:
           raise ValidationError(
               "Текст статьи не должен быть идентичен заголовку."
           )

       return cleaned_data

    def clean_name(self):
       posttitle = self.cleaned_data["posttitle"]
       if posttitle[0].islower():
           raise ValidationError(
               "Название должно начинаться с заглавной буквы"
           )
       return posttitle