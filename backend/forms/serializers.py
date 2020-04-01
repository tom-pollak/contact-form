from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Form
from users.serializers import CustomUserSerializer
from users.models import CustomUser

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('name', 'url', 'test_period', 'email_reminder', 'creation_date', 'active', 'created_by',)
        read_only_fields = ('created_by', 'creation_date',)