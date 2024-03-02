from dj_rest_auth.views import LoginView
from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponse,JsonResponse
from rest_framework.views import APIView




class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

class AddEmplpyee(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = AddEmployeeSerializer

class UpdatePayment(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = UpdatesalarySerializer
    lookup_field = "id"

class ListSalary(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = ListsalarySerializer
    lookup_field = "id"

class ListAllEmployee(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = AddEmployeeSerializer


class RetrieveEmployee(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = AddEmployeeSerializer
    lookup_field = "id"

class AddRemark(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Remarks.objects.all()
    serializer_class = AddRemarkSerializer

class ListRemark(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ListRemarkSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Remarks.objects.filter(employee = user_id )
    
# class ListSalaryPerMonth(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self,request):
#         user_id = self.kwargs.get('id')
        

class AddJobcard(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = JobcardSerializer



class ListJobcards(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = JobcardSerializer

    def get_queryset(self):
        job_type = self.kwargs.get('job_type')

        return JobCard.objects.filter(status = job_type) 

    





