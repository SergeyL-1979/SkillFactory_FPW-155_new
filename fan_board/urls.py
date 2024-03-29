from django.urls import path

from fan_board import views

app_name = 'fan_board'

urlpatterns = [
    path('', views.AdListView.as_view(), name='ads_list'),
    # path('detail/<int:pk>/', views.AdDetailView.as_view(), name='ads_detail'),
    path('detail/<str:headline>/', views.AdDetailView.as_view(), name='ads_detail'),
    path('create/', views.AdCreateView.as_view(), name='ads_create'),
    path('<str:headline>/update/', views.AdUpdateView.as_view(), name='ads_update'),
    path('delete/<str:headline>/', views.AdDeleteView.as_view(), name='ads_delete'),

    path('category/<str:slug>/', views.CategoryAdsView.as_view(), name='category_ads'),

    # path('mark-notification-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),

    path('response/<int:pk>/', views.user_response, name='accepted_answer'),
]
