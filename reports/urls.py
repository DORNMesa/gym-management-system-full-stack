from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_view, name='reports'),
    path('print/', views.print_report, name='print_report'),
]
