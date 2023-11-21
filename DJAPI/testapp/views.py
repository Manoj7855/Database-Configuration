from django.shortcuts import render
from rest_framework . viewsets import ModelViewSet
from testapp.models import Employee
from testapp.serializers import EmployeeSerializer
# Create your views here.

class EmployeeCRUDCBV(ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

