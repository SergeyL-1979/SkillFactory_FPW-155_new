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

    path('private/', views.PrivatePageView.as_view(), name='private_page'),

    path('search/', views.SearchAdsView.as_view(), name='search_results'),

    path('my-ads/', views.MyAdsView.as_view(), name='my_ads'),

    # path('subscribers/', views.FollowUserView.as_view(), name='follow'),
    # path('unsubscribers/', views.UnfollowUserView.as_view(), name='unfollow'),
    path('toggle_subscription/', views.ToggleSubscriptionView.as_view(), name='toggle_subscription'),
]
