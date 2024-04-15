import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from fan_board.filters import AdvertisementFilter
from fan_board.models import Advertisement, Response, Category
from fan_board.forms import AdvertisementForm, ResponseForm, AdvertisementUpdateForm

logger = logging.getLogger(__name__)


class CategoryAdsView(generic.ListView):
    """ Просмотр показа рекламы по категориям. """
    model = Advertisement
    template_name = 'fan_board/category_ads.html'
    context_object_name = 'cat_list'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = 5

    def get_queryset(self):
        """
        Получите набор запросов объектов Advertisement, отфильтрованных по
        название категории объявлений, указанное в параметре URL-slug.

        :return: Queryset of Advertisement objects
        """
        return Advertisement.objects.filter(ad_category__name=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = get_object_or_404(Category, name=self.kwargs['slug'])

        paginator = Paginator(context['cat_list'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['cat_list'] = page_obj
        return context


class AdListView(generic.ListView):
    model = Advertisement
    context_object_name = 'ads_list'
    paginate_by = 3

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
        pk = self.kwargs.get('pk')
        headline = self.kwargs.get('headline')
        # Пытаемся получить объект по первичному ключу (pk)
        if pk:
            queryset = queryset.filter(pk=pk)
        elif headline:
            queryset = queryset.filter(headline=headline)

        # Получаем значение из URL и используем его для фильтрации объявлений
        # headline = self.kwargs.get('headline')
        return get_object_or_404(queryset, headline=headline)

    def get_context_data(self, **kwargs):
        """
        A method to retrieve and return the context data for the view.
        This method takes in keyword arguments (**kwargs) and returns
        a dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        context['ads_list'] = Advertisement.objects.all()
        # context['ad_response'] = Response.objects.filter(ad=self.get_object())
        context['accepted_responses'] = ad.responses.filter(accepted_answer=True)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        """ Handle POST requests. """
        if not request.user.is_authenticated:
            return redirect('users:login')
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

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект объявления
        obj = self.get_object()

        # Проверяем, является ли текущий пользователь автором объявления
        if request.user != obj.ad_author:
            # Если нет, отображаем страницу с сообщением об ошибке
            return HttpResponseForbidden(render(request, 'fan_board/error_page.html'))

        return super().dispatch(request, *args, **kwargs)

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


class PrivatePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'fan_board/private_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Фильтруем отклики по объявлению
        context['responses'] = Response.objects.filter(ad__ad_author=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')

        response = get_object_or_404(Response, id=response_id)

        if action == 'delete':
            if response.ad.ad_author == request.user:
                response.delete()
                messages.success(request, 'Отклик успешно удален.')
            else:
                messages.error(request, 'Вы не можете удалить этот отклик.')
        elif action == 'accept':
            if response.ad.ad_author == request.user:
                response.accepted_answer = True
                response.save()
                messages.success(request, 'Отклик успешно принят.')
            else:
                messages.error(request, 'Вы не можете принять этот отклик.')

        return redirect('fan_board:private_page')


class SearchAdsView(generic.ListView):
    model = Advertisement
    template_name = 'fan_board/search_results.html'
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(ad_author__first_name__icontains=query) |
                Q(ad_author__last_name__icontains=query) |
                Q(ad_author__username__icontains=query) |
                Q(ad_category__name__icontains=query) |
                Q(headline__icontains=query)
            )
        else:
            queryset = Advertisement.objects.none()  # Пустой QuerySet, чтобы не выводить ничего

        return queryset

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            # Если есть параметр 'q' в запросе, значит, это запрос поиска
            # Отображаем шаблон для результатов поиска
            return render(request, 'fan_board/search_results.html', {'object_list': self.get_queryset()})
        else:
            # В противном случае отображаем только форму поиска
            return render(request, 'fan_board/search_form.html')

# class SearchAdsView(generic.ListView):
#     model = Advertisement
#     template_name = 'fan_board/search_results.html'
#     filterset_class = AdvertisementFilter
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.GET.get('q')
#
#         if query:
#             queryset = queryset.filter(
#                 Q(ad_author__first_name__icontains=query) |
#                 Q(ad_category__name__icontains=query) |
#                 Q(headline__icontains=query)
#             )
#
#         return queryset
