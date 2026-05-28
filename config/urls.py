"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from trainer.views import TrainerDashboardView
from placement.views import PlacementDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/mobilization/', include('mobilization.urls')),
    path('api/counselling/', include('counselling.urls')),
    path('api/registration/', include('registration.urls')),
    path('api/teachers/', include('teachers.urls')),
    path('api/batches/', include('batches.urls')),
    path('api/onboarding/', include('onboarding.urls')),
    path('api/dashboard/', include('dashboard.urls')),

    path('api/trainer/', include('trainer.urls')),
    path('api/dashboard/trainer/', TrainerDashboardView.as_view()),

    path('api/dashboard/placement/', PlacementDashboardView.as_view()),
    path('api/placement/', include('placement.urls')),
]
