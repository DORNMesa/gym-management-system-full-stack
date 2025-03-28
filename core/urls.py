from django.contrib import admin
from django.urls import path, include
from . import views
from decorator_include import decorator_include
from django.contrib.auth.decorators import login_required
from .decorators import manager_access
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='login'),
    path('logout/', views.logout, name='logout'),

    path('managerDashboard/', views.managerDashboard, name='managerDashboard'),
    path('employeeDashboard/', views.employeeDashboard, name='employeeDashboard'),
    path('coachDashboard/', views.coachDashboard, name='coachDashboard'),

    path('employeeAttendance/', views.employeeAttendance, name='employeeAttendance'),
    path('coachAttendance/<int:pk>', views.coachAttendance, name='coachAttendance'),

    path('user/', decorator_include(manager_access,"user.urls",namespace="user")),
    path('schedule/', decorator_include(manager_access,"schedule.urls",namespace="schedule")),
    path('equipment/', decorator_include(login_required,"equipment.urls",namespace="equipment")),
    path('package/', decorator_include(manager_access,"package.urls",namespace="package")),
    path('member/', decorator_include(login_required,"member.urls",namespace="member")),
    path('coach/', decorator_include(login_required,"coach.urls",namespace="coach")),
    path('transaction/', decorator_include(manager_access,"transaction.urls",namespace="transaction")),
    path('reports/', include('reports.urls')),
    path('product/', include('product.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
