"""hawkunamatata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from hawkuna import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetCompleteView,PasswordResetConfirmView,PasswordChangeDoneView,PasswordChangeView

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('hawkuna/', include('hawkuna.urls')),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path(
    'logout/',
    LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),
    name='logout'
    ),


    # path('manage/', views.manage, name='manage'),

    #pass reset url`s
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='hawkuna/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/',PasswordChangeView.as_view(), 
        name='password_change'),
    path('password_reset/', PasswordResetView.as_view(template_name='hawkuna/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetCompleteView.as_view(template_name='hawkuna/password_reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='hawkuna/password_change.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='hawkuna/password_reset_complete.html'),
     name='password_reset_complete'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
