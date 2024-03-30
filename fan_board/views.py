import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.core.mail import send_mail
from django.views.generic import FormView

from fan_board.models import Advertisement, Response, Category
from fan_board.forms import AdvertisementForm, ResponseForm, AdvertisementUpdateForm

logger = logging.getLogger(__name__)


class CategoryAdsView(generic.ListView):
    model = Advertisement
    template_name = 'fan_board/category_ads.html'
    context_object_name = 'cat_list'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # category = get_object_or_404(Category, name=self.kwargs['slug'])
        # return Advertisement.objects.filter(ad_category=category)
        return Advertisement.objects.filter(ad_category__name=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = get_object_or_404(Category, name=self.kwargs['slug'])
        return context


class AdListView(generic.ListView):
    model = Advertisement
    context_object_name = 'ads_list'

    def get_category_display(self):
        return self.request.GET.get('category_display')

    def get_context_data(self, **kwargs):
        context = super(AdListView, self).get_context_data(**kwargs)
        # context['cat_list'] = [category[1] for category in Category.choices]
        context['cat_list'] = Category.objects.all()
        return context


class AdDetailView(generic.DetailView):
    """ View for displaying a single advertisement. """
    model = Advertisement
    context_object_name = 'ads_detail'
    template_name = 'fan_board/advertisement_detail.html'
    form_class = ResponseForm

    def get_object(self, queryset=None):
        """ Retrieve and return the object the view is displaying. """
        if queryset is None:
            queryset = self.get_queryset()

        # Получаем значение из URL и используем его для фильтрации объявлений
        headline = self.kwargs.get('headline')
        return get_object_or_404(queryset, headline=headline)

    def get_context_data(self, **kwargs):
        """
        A method to retrieve and return the context data for the view.
        This method takes in keyword arguments (**kwargs) and returns
        a dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context['ads_list'] = Advertisement.objects.all()
        context['ad_response'] = Response.objects.filter(ad=self.get_object())
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        """ Handle POST requests. """
        form = self.form_class(request.POST)
        if form.is_valid():
            # Сохраняем отклик в базу данных
            response = form.save(commit=False)
            response.ad = self.get_object()
            response.user_answer = request.user
            response.save()
            return redirect('fan_board:ads_detail', headline=self.get_object().headline)
        else:
            # Если форма не допустима, повторно отображаем страницу с формой и ошибками
            return self.render_to_response(self.get_context_data(form=form))


class AdCreateView(LoginRequiredMixin, generic.CreateView):
    model = Advertisement
    form_class = AdvertisementForm

    def form_valid(self, form):
        form.instance.ad_author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Получаем созданный объект объявления
        created_ad = self.object
        # Формируем URL на основе заголовка объявления
        return reverse('fan_board:ads_detail', kwargs={'headline': created_ad.headline})


class AdUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Advertisement
    form_class = AdvertisementUpdateForm
    template_name = 'fan_board/advertisement_update_form.html'

    def form_valid(self, form):
        form.instance.ad_author = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        # Получаем значение заголовка из адресной строки
        headline = self.kwargs.get('headline')
        # Получаем объект объявления по заголовку
        obj = Advertisement.objects.get(headline=headline)
        return obj

    def get_success_url(self):
        # Получаем созданный объект объявления
        created_ad = self.object
        # Формируем URL на основе заголовка объявления
        return reverse('fan_board:ads_detail', kwargs={'headline': created_ad.headline})


class AdDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Advertisement
    success_url = '/mmorpg/'

    def get_object(self, queryset=None):
        # Получаем значение заголовка из адресной строки
        headline = self.kwargs.get('headline')
        # Получаем объект объявления по заголовку
        obj = Advertisement.objects.get(headline=headline)
        return obj


# @login_required(login_url='/account/login/')
# def user_response(request, pk):
#     """Отправка отклик по объявлению на пост"""
#     user_res = get_object_or_404(Response, id=request.POST.get('response_id'))
#     user_res.accepted_answer.add(request.user)
#     messages.info(request, 'Отклик успешно отправлен!')
#     print(f'{request.user} отправил отклик на объявление "{user_res.ad.headline}"')
#     print()
#     return redirect('post_detail', pk=pk)

