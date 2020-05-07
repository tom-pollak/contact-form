from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Form, Submission
from users.serializers import CustomUserSerializer
from users.models import CustomUser


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('form', 'form_submitted',)


class FormSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Form
        fields = ('id', 'name', 'url', 'test_period', 'email_reminder',
                  'creation_date', 'created_by', 'active',
                  'confirmed', 'last_submitted', 'submission'
                  )

        read_only_fields = ('created_by', 'creation_date', 'submission')

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['created_by'] = user
        name = attrs.get('name')
        url = attrs.get('url')

        name_obj = Form.objects.filter(created_by=user, name=name).first()
        url_obj = Form.objects.filter(created_by=user, url=url).first()

        if not name_obj and not url_obj:
            return attrs

        elif (name_obj and name_obj.id == attrs.get('id')) or (url_obj and url_obj.id == attrs.get('id')):
            print('hererere')
            return attrs

        else:
            msg = {}
            if name_obj:
                msg['name'] = 'You have already created a form with that name.'
            if url_obj:
                msg['url'] = 'You have already created a form with that URL.'
            raise serializers.ValidationError(msg)
