from django.urls import path
from . import views

app_name = 'leaves'

urlpatterns = [
    path('', views.leave_list, name='list'),
    path('apply/', views.leave_apply, name='apply'),
    path('<int:pk>/<str:action>/', views.leave_review, name='review'),
]
