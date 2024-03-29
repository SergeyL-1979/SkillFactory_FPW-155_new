from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import Advertisement, Response


class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['ad_category', 'headline', 'content']

    def __init__(self, *args, **kwargs):
        """ Обновление стилей формы под Bootstrap. """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False

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
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'cols': 50,
                    'placeholder': 'Введите ваш отклик здесь не менее 10 символов',
                }
            ),
        }
        labels = {
            'text': 'Отклик',
        }

