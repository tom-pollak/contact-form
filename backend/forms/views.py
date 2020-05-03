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

    @transaction.atomic
    def handle_integrity(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(created_by=self.request.user)
            return None

        except IntegrityError as err:
            return err

    def error_msg(self, err):
        msg = {}
        if err:
            if 'name' in str(err):
                msg['name'] = ['You have already created a form with that name']
            if 'url' in str(err):
                msg['url'] = ['You have already created a form with that url']
            raise ValidationError(msg, code=400)

    def get_queryset(self):
        user = self.request.user
        return Form.objects.filter(created_by=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        err = self.handle_integrity(serializer)
        self.error_msg(err)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        err = self.handle_integrity(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        self.error_msg(err)
        return Response(serializer.data)


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
