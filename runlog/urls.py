from django.contrib import admin
from django.urls import path

from runs import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'login/',
        views.CustomLoginView.as_view(),
        name='login',
    ),

    path(
        'logout/',
        views.CustomLogoutView.as_view(),
        name='logout',
    ),

    path(
        'register/',
        views.register,
        name='register',
    ),

    path(
        'edit/<int:run_id>/',
        views.edit_run,
        name='edit_run',
    ),

    path(
        'delete/<int:run_id>/',
        views.delete_run,
        name='delete_run',
    ),

    path(
        '',
        views.home,
        name='home',
    ),
]