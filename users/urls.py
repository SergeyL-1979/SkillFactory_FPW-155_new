from allauth.account.views import SignupForm, LoginView, LogoutView
from django.urls import path
from .views import UserProfile, UserProfileEdit, ConfirmUser

app_name = 'users'

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='profile'),
    path('edit/<int:pk>/', UserProfileEdit.as_view(), name='edit_profile'),
    path('signup/', SignupForm, name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
]
