"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import CustomUserSerializer


class CreateCustomUserAPIView(APIView):
    permission_classes = (AllowAny,)
 
    def post(self, request):
        user = request.data
        serializer = CustomUserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""