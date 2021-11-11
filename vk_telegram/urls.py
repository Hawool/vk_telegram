from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from vk_telegram import views

urlpatterns = [
    path('message/', views.CreateView.as_view()),  #
    path('message/all', views.ListView.as_view()),  #
]

urlpatterns = format_suffix_patterns(urlpatterns)