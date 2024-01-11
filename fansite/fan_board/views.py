from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.mail import send_mail
from django.views.generic import FormView

from .models import Advertisement, Response, Category
from .forms import AdvertisementForm, ResponseForm


class CategoryAdsView(generic.ListView):
    model = Advertisement
    template_name = 'fan_board/category_ads.html'
    context_object_name = 'cat_list'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    # def get_queryset(self):
    #     category_slug = self.kwargs.get('category')
    #     # Get the integer value for the given category slug
    #     category_int = getattr(Category, category_slug, None)
    #     if category_int is not None:
    #         # Filter advertisements based on the category
    #         return Advertisement.objects.filter(category=category_int)
    #     else:
    #         # Handle the case where the category is not found
    #         return Advertisement.objects.none()

    def get_context_data(self, **kwargs):
        context = super(CategoryAdsView, self).get_context_data(**kwargs)
        category_name = [category for category in Category.choices]
        # category_slug = self.kwargs.get('category')
        # # category = get_object_or_404(Category, slug=category_slug)
        # category = Advertisement.objects.get(category=category_slug)
        context['category_name'] = category_name
        return context


class AdListView(generic.ListView):
    model = Advertisement
    context_object_name = 'ads_list'

    def get_category_display(self):
        return self.request.GET.get('category_display')

    def get_context_data(self, **kwargs):
        context = super(AdListView, self).get_context_data(**kwargs)
        context['cat_list'] = [category[1] for category in Category.choices]
        return context


class AdDetailView(generic.DetailView):
    model = Advertisement
    context_object_name = 'ads_detail'

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        context['ads_list'] = Advertisement.objects.all()
        return context


class AdCreateView(generic.CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    success_url = '/ads/'

    """ Функция для кастомный валидации полей формы модели """
    def form_valid(self, form):
        # Создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через request передаем недостающую форму, которая обязательно
        # делаем на моменте авторизации и создании прав стать автором
        fields.user = self.request.user
        """ Наконец сохраняем в БД """
        fields.save()
        return super().form_valid(form)


# class ResponseListView(generic.ListView):
#     model = Response
#     context_object_name = 'responses_list'
#
#     def get_context_data(self, **kwargs):
#         context = super(ResponseListView, self).get_context_data(**kwargs)
#         context['responses_list'] = Response.objects.all()














# class AdvertisementController:
#     def create_advertisement(self, request):
#         # Implement logic for creating advertisements
#         pass
#
#     def edit_advertisement(self, request, ad_id):
#         # Implement logic for editing advertisements
#         pass
#
#     def delete_advertisement(self, request, ad_id):
#         # Implement logic for deleting advertisements
#         pass
#
#
# class ResponseController:
#     def respond_to_advertisement(self, request, ad_id):
#         # Implement logic for responding to advertisements
#         pass
#
#     def private_page(self, request):
#         # Implement logic for the private page with responses
#         pass
#
#     def send_response_notification(self, user, advertisement):
#         # Implement logic for sending email notification to the user
#         pass


# def create_advertisement(request):
#     # Implement logic for creating advertisements
#
# def edit_advertisement(request, ad_id):
#     # Implement logic for editing advertisements
#
# def delete_advertisement(request, ad_id):
#     # Implement logic for deleting advertisements
#
# def respond_to_advertisement(request, ad_id):
#     # Implement logic for responding to advertisements
#
# def private_page(request):
#     # Implement logic for the private page with responses

