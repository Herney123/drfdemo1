from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from stuapi.models import Student
from students.serializers import StudentModelSerializer


class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
