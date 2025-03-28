from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .decorators import manager_access
from decorator_include import decorator_include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='login'),
    path('logout/', views.logout, name='logout'),

    path('managerDashboard/', views.managerDashboard, name='managerDashboard'),
    path('employeeDashboard/', views.employeeDashboard, name='employeeDashboard'),
    path('coachDashboard/', views.coachDashboard, name='coachDashboard'),

    path('employeeAttendance/', views.employeeAttendance, name='employeeAttendance'),
    path('coachAttendance/<int:pk>', views.coachAttendance, name='coachAttendance'),

    path('user/', decorator_include(manager_access, 'user.urls')),
    path('schedule/', decorator_include(manager_access, 'schedule.urls')),
    path('equipment/', decorator_include(login_required, 'equipment.urls')),
    path('package/', decorator_include(manager_access, 'package.urls')),
    path('member/', decorator_include(login_required, 'member.urls')),
    path('coach/', decorator_include(login_required, 'coach.urls')),
    path('transaction/', decorator_include(manager_access, 'transaction.urls')),
    path('reports/', decorator_include(login_required, 'reports.urls')),
    path('product/', include('product.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
