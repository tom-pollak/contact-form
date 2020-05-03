from django.urls import path, include
from rest_framework_nested import routers

from forms.views import FormViewSet, SubmissionViewSet

router = routers.SimpleRouter()
router.register(r'forms', FormViewSet, basename='form')

forms_router = routers.NestedSimpleRouter(router, r'forms', lookup='form')
forms_router.register(r'submissions', SubmissionViewSet, basename='submission')
