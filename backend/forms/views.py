from django.db.utils import IntegrityError
from django.db import transaction

from rest_framework import viewsets, status, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError

from .models import Form, Submission
from .serializers import FormSerializer, SubmissionSerializer


class IsOwnerOfSubmission(permissions.BasePermission):

    def has_permission(self, request, view):
        form = Form.objects.get(pk=view.kwargs['form_pk'])
        if form.created_by == request.user:
            return True
        raise NotFound


class FormViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FormSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        user = self.request.user
        return Form.objects.filter(created_by=user)


class SubmissionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOfSubmission,)

    def perform_create(self, serializer):
        form_pk = self.kwargs['form_pk']
        form = Form.objects.get(pk=form_pk)
        serializer.save(form=form)

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(form__created_by=user)
