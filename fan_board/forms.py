from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import Advertisement, Response


class AdvertisementForm(forms.ModelForm):
    # text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'category']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
