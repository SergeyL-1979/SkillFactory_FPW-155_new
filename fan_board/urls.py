from django.urls import path

from fan_board import views

app_name = 'fan_board'

urlpatterns = [
    path('', views.AdListView.as_view(), name='ads_list'),
    path('detail/<int:pk>/', views.AdDetailView.as_view(), name='ads_detail'),
    path('create/', views.AdCreateView.as_view(), name='ads_create'),

    path('category/<str:slug>/', views.CategoryAdsView.as_view(), name='category_ads'),
]


# urlpatterns = [
#     path('create/', advertisement_controller.create_advertisement, name='create_advertisement'),
#     path('edit/<int:ad_id>/', advertisement_controller.edit_advertisement, name='edit_advertisement'),
#     path('delete/<int:ad_id>/', advertisement_controller.delete_advertisement, name='delete_advertisement'),
#
#     path('respond/<int:ad_id>/', response_controller.respond_to_advertisement, name='respond_to_advertisement'),
#     path('private/', response_controller.private_page, name='private_page'),
# ]
