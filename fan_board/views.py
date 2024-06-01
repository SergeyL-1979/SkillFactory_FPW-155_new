import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from fan_board.filters import AdvertisementFilter
from fan_board.models import Advertisement, Response, Category, Subscription
from fan_board.forms import AdvertisementForm, ResponseForm, AdvertisementUpdateForm, SubscriptionForm
from mmorpg_fansite import settings

logger = logging.getLogger(__name__)


class CategoryAdsView(generic.ListView):
    """ View advertising displays by category. """
    model = Advertisement
    template_name = 'fan_board/category_ads.html'
    context_object_name = 'cat_list'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = 5

    def get_queryset(self):
        """
        Retrieves the queryset of advertisements based on the specified slug.

        Returns:
            QuerySet: The queryset of advertisements filtered by the ad category name.
        """
        return Advertisement.objects.filter(ad_category__name=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the view.
        This method overrides the `get_context_data` method of the parent class to add additional
        data to the context. It retrieves the category name based on the slug provided in
        the URL parameters. It also paginates the `cat_list` based on the `paginate_by` attribute of
        the class. The current page number is obtained from the query parameters.
        The paginated `cat_list` is added to the context, along with the category name.

        Parameters:
            **kwargs (dict): Additional keyword arguments.

        Returns:
            dict: The updated context data.
        """
        context = super().get_context_data(**kwargs)
        context['category_name'] = get_object_or_404(Category, name=self.kwargs['slug'])

        paginator = Paginator(context['cat_list'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['cat_list'] = page_obj
        return context


class AdListView(generic.ListView):
    """ View for displaying a list of advertisements. """
    model = Advertisement
    context_object_name = 'ads_list'
    paginate_by = 3

    def get_category_display(self):
        """
        Returns the value of the 'category_display' query parameter from the current request's GET parameters.

        :return: The value of the 'category_display' query parameter as a string, or None if it is not present.
        """
        return self.request.GET.get('category_display')

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional keyword arguments.
        :return: The context data dictionary.
        """
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

        if pk:
            queryset = queryset.filter(pk=pk)
        elif headline:
            queryset = queryset.filter(headline=headline)

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
            response = form.save(commit=False)
            response.ad = self.get_object()
            response.user_answer = request.user
            response.save()
            return redirect('fan_board:ads_detail', headline=self.get_object().headline)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class AdCreateView(LoginRequiredMixin, generic.CreateView):
    """ View for creating a new advertisement. """
    model = Advertisement
    form_class = AdvertisementForm

    def form_valid(self, form):
        """
        Sets the `ad_author` attribute of the `form.instance` object to the currently logged-in
        user and calls the `form_valid` method of the parent class with the provided `form` parameter.

        Parameters:
            form (Form): The form instance to be validated.

        Returns:
            HttpResponse: The response returned by the `form_valid` method of the parent class.
        """
        form.instance.ad_author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Retrieves the success URL for the current object.

        Returns:
            str: The success URL for the created ad, based on the headline of the ad.
        """
        created_ad = self.object
        return reverse('fan_board:ads_detail', kwargs={'headline': created_ad.headline})


class AdUpdateView(LoginRequiredMixin, generic.UpdateView):
    """ View for updating an existing advertisement. """
    model = Advertisement
    form_class = AdvertisementUpdateForm
    template_name = 'fan_board/advertisement_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches the request to the appropriate handler method.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
        obj = self.get_object()

        if request.user != obj.ad_author:
            return HttpResponseForbidden(render(request, 'fan_board/error_page.html'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Check if the form is valid and assign the ad_author as the
        current user before calling the parent class's form_valid method.
        """
        form.instance.ad_author = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """
        Retrieves an object from the database based on the provided headline.

        Parameters:
            queryset (QuerySet, optional): The queryset to retrieve the object from. Defaults to None.

        Returns:
            Advertisement: The retrieved Advertisement object.
        """
        headline = self.kwargs.get('headline')
        obj = Advertisement.objects.get(headline=headline)
        return obj

    def get_success_url(self):
        """
        Retrieves the success URL for the current object.

        Returns:
            str: The success URL for the created ad, based on the headline of the ad.
        """
        created_ad = self.object
        return reverse('fan_board:ads_detail', kwargs={'headline': created_ad.headline})


class AdDeleteView(LoginRequiredMixin, generic.DeleteView):
    """ View for deleting an existing advertisement. """
    model = Advertisement
    success_url = '/'

    def get_object(self, queryset=None):
        # Получаем значение заголовка из адресной строки
        headline = self.kwargs.get('headline')
        # Получаем объект объявления по заголовку
        obj = Advertisement.objects.get(headline=headline)
        return obj


class PrivatePageView(LoginRequiredMixin, generic.TemplateView):
    """ View for displaying private page. """
    template_name = 'fan_board/private_page.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data for the view.
        This method is responsible for retrieving the context data for the view.
        It calls the `get_context_data` method of the parent class and adds the
        filtered responses to the context. The filtered responses are obtained
        by filtering the `Response` objects based on the `ad__ad_author` field,
        which is compared to the `request.user` attribute of the current request.

        Parameters:
            **kwargs (dict): Additional keyword arguments.

        Returns:
            dict: The context data for the view, including the filtered responses.
        """
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(ad__ad_author=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request for the given view.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: A redirect response to the 'fan_board:private_page' URL.

        Raises:
            Http404: If the response with the given ID is not found.

        Description:
            This function handles the POST request for the view. It retrieves the 'response_id' and 'action'
            parameters from the request's POST data. It then retrieves the Response object with the given ID.

            If the 'action' parameter is 'delete', it checks if the response's ad author is the same as the
            request user. If so, it deletes the response, displays a success message, and redirects to the
            'fan_board:private_page' URL. Otherwise, it displays an error message.

            If the 'action' parameter is 'accept', it checks if the response's ad author is the same as the
            request user. If so, it sets the 'accepted_answer' attribute of the response to True, saves the
            response, displays a success message, and redirects to the 'fan_board:private_page' URL. Otherwise,
            it displays an error message.

            If the response with the given ID is not found, it raises an Http404 exception.

        Note:
            This function assumes that the necessary imports and middleware have been set up correctly.

        Example Usage:
            response = self.post(request, *args, **kwargs)
        """
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


class MyAdsView(generic.ListView):
    """ View for displaying my ads. """
    model = Advertisement
    template_name = 'fan_board/my_ads.html'

    def get_queryset(self):
        return Advertisement.objects.filter(ad_author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_ads'] = self.get_queryset()
        return context


class SearchAdsView(generic.ListView):
    """ View for searching ads. """
    model = Advertisement
    template_name = 'fan_board/search_results.html'
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        """
        A method that filters the queryset based on a search query parameter
        in the request.
        """
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
        """
        A description of the entire function, its parameters, and its return types.
        """
        if 'q' in self.request.GET:
            # Если есть параметр 'q' в запросе, значит, это запрос поиска
            # отображаем шаблон для результатов поиска
            return render(request, 'fan_board/search_results.html', {'object_list': self.get_queryset()})
        else:
            # В противном случае отображаем только форму поиска
            return render(request, 'fan_board/search_form.html')


# ============ РЕАЛИЗАЦИЯ ПОДПИСКИ,ОТПИСКИ ОТ РАССЫЛКИ ================
class FollowUserView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_subscription, created = Subscription.objects.get_or_create(user=user)
        user_subscription.subscribed = True
        user_subscription.save()

        # Отправка уведомления об успешной подписке
        send_mail(
            subject='Подписка на рассылку',
            message='Вы подписались на рассылку новых объявлений.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        print('Подписка активирована')
        # return redirect(request.META.get('HTTP_REFERER'))
        # Передача статуса подписки в контекст шаблона
        return render(request, "fan_board/advertisement_list.html", {'is_subscribed': True})


class UnfollowUserView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user_subscription, created = Subscription.objects.get_or_create(user=user)
        user_subscription.subscribed = False
        user_subscription.save()

        # Отправка уведомления об успешной подписке
        send_mail(
            subject='Отписка от рассылки',
            message=f'Вы отписались от рассылки новых объявлений.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        print('Подписка деактивирована')
        # return redirect(request.META.get('HTTP_REFERER'))
        # Передача статуса подписки в контекст шаблона
        return render(request, "fan_board/advertisement_list.html", {'is_subscribed': False})
