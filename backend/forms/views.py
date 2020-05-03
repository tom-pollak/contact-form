from django.shortcuts import render
from django.db.utils import IntegrityError
from django.db import transaction

from rest_framework import viewsets, status, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Form, Submission
from .serializers import FormSerializer, SubmissionSerializer


class IsOwnerOfSubmission(permissions.BasePermission):

    def has_permission(self, request, view):
        form = Form.objects.get(pk=view.kwargs['form_pk'])
        return form.created_by == request.user


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
        msg = None
        if err:
            if 'name' in str(err):
                err = 'name'
            elif 'url' in str(err):
                err = 'url'
            else:
                raise Exception('Error can\'t be identified: \n%s' % (err))

            msg = 'User already created a form with that %s.' % (err)
        return err, msg

    def get_queryset(self):
        user = self.request.user
        return Form.objects.filter(created_by=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        err = self.handle_integrity(serializer)
        if err:
            err, msg = self.error_msg(err)
            return Response({err: msg}, status=status.HTTP_400_BAD_REQUEST)

        else:
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

        err, msg = self.error_msg(err)
        if msg:
            return Response({err: msg}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.data)


class SubmissionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOfSubmission,)

    def get_queryset(self, request, *args, **kwargs):
        print('got here')
        form_pk = self.kwargs['form_pk']
        return Submission.objects.filter(form_id=form_pk)

    def perform_create(self, serializer):
        form_pk = self.kwargs['form_pk']
        form = Form.objects.get(pk=form_pk)
        serializer.save(form=form)
