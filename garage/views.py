from dj_rest_auth.views import LoginView
from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum


# pylint: disable=E1101,W0702


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        print("innn")
        response = super().get_response()

        if response.status_code == status.HTTP_200_OK:
            user_data = UserSerializer(self.user).data
            response.data["user"] = user_data

            refresh = RefreshToken.for_user(self.user)
            response.data["refresh"] = str(refresh)
            response.data["access"] = str(refresh.access_token)
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
        user_id = self.kwargs.get("id")
        return Remarks.objects.filter(employee=user_id)


# class ListSalaryPerMonth(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self,request):
#         user_id = self.kwargs.get('id')


class AddJobcard(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = AddJobCardSerializer


class ListJobcards(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveJobSerializer

    def get_queryset(self):
        job_type = self.request.query_params.get("status")

        return JobCard.objects.filter(status=job_type)


class RetrieveJobs(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = RetrieveJobSerializer
    lookup_field = "id"


class UpdateJobsClose(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = JobcardSerializer
    lookup_field = "id"


class UpdateJobs(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = AddJobCardSerializer
    lookup_field = "id"


class AddTechnician(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Technician.objects.all()
    serializer_class = TechnicianAddSerializer


class UpdateTechnician(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Technician.objects.all()
    serializer_class = TechnicianAddSerializer
    lookup_field = "id"


class DeleteTechniciane(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Technician.objects.all()
    serializer_class = TechnicianAddSerializer
    lookup_field = "id"


class ListTechnician(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TechnicianSerializer

    def get_queryset(self):
        job = self.request.query_params.get("job")
        job_card = JobCard.objects.get(id=job)
        return Technician.objects.filter(job_card=job_card)


class AddSpareparts(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SpareParts.objects.all()
    serializer_class = SparePartsAddSerializer


class UpdateSpareparts(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SpareParts.objects.all()
    serializer_class = SparePartsAddSerializer
    lookup_field = "id"


class DeleteSpareparts(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SpareParts.objects.all()
    serializer_class = SparePartsAddSerializer
    lookup_field = "id"


class ListSpareparts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SparePartsSerializer

    def get_queryset(self):
        job = self.request.query_params.get("job")
        job_card = JobCard.objects.get(id=job)
        return SpareParts.objects.filter(job_card=job_card)


class AddIssues(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Issues.objects.all()
    serializer_class = IssuesAddSerializer


class UpdateIssues(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Issues.objects.all()
    serializer_class = IssuesAddSerializer
    lookup_field = "id"


class DeleteIssues(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Issues.objects.all()
    serializer_class = IssuesAddSerializer
    lookup_field = "id"


class ListIssues(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IssuesSerializer

    def get_queryset(self):
        job = self.request.query_params.get("job")
        job_card = JobCard.objects.get(id=job)
        return Issues.objects.filter(job_card=job_card)


class ListBranch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class ListJobType(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer


class SpareAmount(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        job_card = self.request.query_params.get("job_card")
        job_card_obj = JobCard.objects.get(id=job_card)
        cabin_ac = JobType.objects.get(name="Cabin Ac")
        reefer_unit = JobType.objects.get(name="Reefer Unit")
        ref_body_work = JobType.objects.get(name="Ref Body Work")
        chiller_unit = JobType.objects.get(name="Chiller Unit")

        spare_cabin_ac = SpareParts.objects.filter(
            job_card=job_card_obj, job_type=cabin_ac
        ).aggregate(spare_cabin_ac=Sum("cost"))["spare_cabin_ac"]
        spare_reefer_unit = SpareParts.objects.filter(
            job_card=job_card_obj, job_type=reefer_unit
        ).aggregate(spare_reefer_unit=Sum("cost"))["spare_reefer_unit"]
        spare_ref_body_work = SpareParts.objects.filter(
            job_card=job_card_obj, job_type=ref_body_work
        ).aggregate(spare_ref_body_work=Sum("cost"))["spare_ref_body_work"]
        spare_chiller_unit = SpareParts.objects.filter(
            job_card=job_card_obj, job_type=chiller_unit
        ).aggregate(spare_chiller_unit=Sum("cost"))["spare_chiller_unit"]
        total = (
            spare_cabin_ac
            + spare_reefer_unit
            + spare_ref_body_work
            + spare_chiller_unit
        )
        spare_cost = {
            "spare_cabin_ac": spare_cabin_ac,
            "spare_reefer_unit": spare_reefer_unit,
            "spare_ref_body_work": spare_ref_body_work,
            "spare_chiller_unit": spare_chiller_unit,
            "total_amount": total,
        }
        return Response(spare_cost)


class ListOtherExpense(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OtherExpenseSerializer

    def get_queryset(self):
        job_card = self.request.query_params.get("job_card")
        return OtherExpense.objects.filter(job_card=job_card)


class AddOtherExpense(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OtherExpense.objects.all()
    serializer_class = OtherExpenseSerializer


class TotalExpense(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        job_card = self.request.query_params.get("job_card")
        job_card_obj = JobCard.objects.get(id=job_card)
        total_spare_cost = SpareParts.objects.filter(job_card=job_card_obj).aggregate(
            total_spare_cost=Sum("cost")
        )["total_spare_cost"]
        total_other_expense_cost = OtherExpense.objects.filter(
            job_card=job_card_obj
        ).aggregate(total_other_expense_cost=Sum("amount"))["total_other_expense_cost"]
        total = {
            "total_amount": total_spare_cost + total_other_expense_cost,
        }
        return Response(total)


class ListCustomers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListCustomerSerializer

    def get_queryset(self):
        customer_type = self.request.query_params.get("customer_type")
        if customer_type:
            return Customer.objects.filter(customer_type=customer_type)
        return Customer.objects.all()


class AddCustomers(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = AddCustomerSerializer


class UpdateCustomer(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "id"


class DeleteCustomer(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "id"


class AddExpense(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = AddExpenseSerializer


class ListExpense(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddExpenseSerializer

    def get_queryset(self):
        type = self.request.query_params.get("type")
        if type:
            return Expense.objects.filter(type=type)
        return Customer.objects.all()


class UpdateExpense(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = AddExpenseSerializer
    lookup_field = "id"


class DeleteExpense(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = AddExpenseSerializer
    lookup_field = "id"


class AddIncome(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()
    serializer_class = AddIncomeSerializer


class ListIncome(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddIncomeSerializer

    def get_queryset(self):
        type = self.request.query_params.get("type")
        if type:
            return Income.objects.filter(type=type)
        return Income.objects.all()


class UpdateIncome(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()
    serializer_class = AddIncomeSerializer
    lookup_field = "id"


class DeleteIncome(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = AddIncomeSerializer
    lookup_field = "id"
