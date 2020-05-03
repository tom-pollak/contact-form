from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Form, Submission
from users.serializers import CustomUserSerializer
from users.models import CustomUser


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('form',)


class FormSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Form
        fields = ('id', 'name', 'url', 'test_period', 'email_reminder',
                  'creation_date', 'created_by', 'active', 'active',
                  'confirmed', 'last_submitted', 'submissions'
                  )

        read_only_fields = ('created_by', 'creation_date', 'submissions')
