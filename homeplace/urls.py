"""
URL configuration for homeplace project.

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
from django.conf.urls import include
from django.urls import path
from homeplaceapi.views import register_user, login_user, PropertyView, SwapperView, AreaView, PaymentTypeView
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'properties',PropertyView, 'property')
router.register(r'swappers',SwapperView, 'swapper')
router.register(r'areas',AreaView, 'area')
router.register(r'paymenttypes',PaymentTypeView, 'paymenttype')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]