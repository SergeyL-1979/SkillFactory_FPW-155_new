import logging

from allauth.account.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render

from users.models import CustomUser
from users.forms import UserForm
from fan_board.models import Advertisement

logger = logging.getLogger(__name__)


class UserProfile(LoginRequiredMixin, DetailView):
    """Кабинет пользователя"""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.object.pk})

    def handle_response(self, post, username, message):
        user = get_object_or_404(CustomUser, username=username)
        post.responses.remove(user)
        messages.info(self.request, message)

    def post(self, request, *args, **kwargs):
        if request.POST.get('accept_response'):
            accept_data = request.POST.get('accept_response').split(' ')
            logger.info(f"Accept {accept_data}")
            post = get_object_or_404(Advertisement, id=accept_data[-1])
            self.handle_response(post, accept_data[0], 'Вы приняли отклик!')
        elif request.POST.get('deny_response'):
            deny_data = request.POST.get('deny_response').split(' ')
            post = get_object_or_404(Advertisement, id=deny_data[-1])
            self.handle_response(post, deny_data[0], 'Вы отклонили отклик!')
        return redirect('profile')


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    """Кабинет пользователя"""
    form_class = UserForm
    template_name = 'users/edit_profile.html'
    login_url = '/account/login/'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')  # Получаем 'pk' из URL-параметра
        return get_object_or_404(CustomUser, pk=pk)

    def get_success_url(self):
        user = self.get_object()
        return reverse_lazy('users:profile')


class ConfirmUser(UpdateView):
    model = CustomUser
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'activation_code' in request.POST:
            user = CustomUser.objects.filter(activation_code=request.POST['activation_code'])
            if user.exists():
                user.update(is_active=True)
                user.update(is_staff=True)
                user.update(activation_code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
        return redirect('/account/login/')
