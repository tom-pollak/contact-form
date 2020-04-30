from django.db import models
from django.core.validators import RegexValidator


class Form(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    test_period = models.PositiveSmallIntegerField(default=7)
    email_reminder = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    last_submitted = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['created_by', 'name'], name='created-name'),
            models.UniqueConstraint(
                fields=['created_by', 'url'], name='created-url'),
        ]

    def __str__(self):
        return self.name


class Submissions(models.Model):
    form = models.ForeignKey('Form', on_delete=models.CASCADE)
    key = models.CharField(max_length=50, unique=True)
    form_submitted = models.DateTimeField(auto_now_add=True)
    form_recieved = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.form) + '_' + self.form_submitted.date
