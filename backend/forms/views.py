from django.shortcuts import render
from django.db.utils import IntegrityError

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Form
from .serializers import FormSerializer

class FormViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FormSerializer

    def get_queryset(self):
        user = self.request.user
        return Form.objects.filter(created_by=user)

    def perform_create(self, serializer):
        try:
            serializer.save(created_by=self.request.user)
            return None

        except IntegrityError as err:
            return err

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        err = self.perform_create(serializer)
        if err:
            if 'name' in str(err):
                err = 'name'
            elif 'url' in str(err):
                err = 'url'
            else:
                raise Exception('Error can\'t be identified: \n%s'%(err))

            msg = 'User already created a form with that %s.'%(err)

            return Response({err: msg}, status=status.HTTP_400_BAD_REQUEST)

        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)