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
from rest_framework_simplejwt.tokens import RefreshToken




class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    def get_response(self):
        print("innn")
        response = super().get_response()
        
        if response.status_code == status.HTTP_200_OK:
            user_data = UserSerializer(self.user).data
            response.data["user"] = user_data

            refresh = RefreshToken.for_user(self.user)
            response.data['refresh'] = str(refresh)
            response.data['access'] = str(refresh.access_token)
        return response 
    
class RetrieveUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    
class AddEmplpyee(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = AddEmployeeSerializer
    
class UpdatePayment(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = UpdatesalarySerializer
    lookup_field = "id"

class ListSalary(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = ListsalarySerializer
    lookup_field = "id"

class ListAllEmployee(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = AddEmployeeSerializer


class RetrieveEmployee(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = AddEmployeeSerializer
    lookup_field = "id"

class AddRemark(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Remarks.objects.all()
    serializer_class = AddRemarkSerializer

class ListRemark(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListRemarkSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Remarks.objects.filter(employee = user_id )
    
# class ListSalaryPerMonth(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self,request):
#         user_id = self.kwargs.get('id')
        

class AddJobcard(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = JobcardSerializer



class ListJobcards(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobcardSerializer

    def get_queryset(self):
        job_type = self.request.query_params.get('status')
        return JobCard.objects.filter(status = job_type) 

    

class RetrieveJobs(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = JobcardSerializer
    lookup_field = "id"

class UpdateJobs(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = JobcardSerializer
    lookup_field = "id"

class AddTechnician(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer


class UpdateTechnician(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    lookup_field = "id"

class DeleteTechniciane(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    lookup_field = "id"


class AddSpareparts(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SpareParts.objects.all()
    serializer_class = SparePartsSerializer


class UpdateSpareparts(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SpareParts.objects.all()
    serializer_class = SparePartsSerializer
    lookup_field = "id"

class DeleteSpareparts(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SpareParts.objects.all()
    serializer_class = SparePartsSerializer
    lookup_field = "id"


class AddIssues(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer


class UpdateIssues(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    lookup_field = "id"

class DeleteIssues(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    lookup_field = "id"

