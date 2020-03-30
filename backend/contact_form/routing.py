from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path

from forms.views import FormViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet, basename='form')
