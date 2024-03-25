from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import Advertisement, Response


class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['headline', 'content', 'ad_category', ]

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_headline(self):
        headline = self.cleaned_data['headline']
        queryset = Advertisement.objects.filter(headline=headline)

        # Проверяем, существует ли объявление с таким же заголовком
        if queryset.exists():
            # Проверяем, является ли текущее редактируемое объявление одним из найденных
            if self.instance and queryset.exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Этот заголовок уже используется. Пожалуйста, выберите другой.")
            elif not self.instance:
                raise forms.ValidationError("Этот заголовок уже используется. Пожалуйста, выберите другой.")
        return headline
        # if Advertisement.objects.filter(headline=headline).exists():
        #     raise forms.ValidationError("Этот заголовок уже используется. Пожалуйста, выберите другой.")
        # return headline


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
