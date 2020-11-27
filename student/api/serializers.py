from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Avg, Max
from django.dispatch import receiver
from django.template.backends import django
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import   Course


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

