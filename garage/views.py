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
from django.utils import timezone
import logging




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
            
            session = self.request.session
            session['account_id'] = str(self.user.account.id) if self.user.account else None
            session['branch_id'] = str(self.user.branch.id) if self.user.branch else None
            session['team_id'] = str(self.user.team.id) if self.user.team else None
            session.save()
            logger = logging.getLogger('django')
            logger.debug(f"Account ID in session: {self.request.session.get('account_id')}")
    

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
    serializer_class = AddEmployeeSerializer
    
    def get_queryset(self):
         
         account_id = self.request.session.get('account_id') 
         branch_id = self.request.session.get('branch_id') 
         if branch_id:
            return Employee.objects.filter(branch_id=branch_id)

         elif account_id:
            branches = Branch.objects.filter(account_id=account_id).values_list('id', flat=True)
            return Employee.objects.filter(branch_id__in=branches)

         else:
            
            return Employee.objects.none()


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
        account_id = self.request.session.get('account_id') 
        branch_id = self.request.session.get('branch_id') 
        if branch_id:
            return JobCard.objects.filter(status=job_type,branch_id=branch_id)

        elif account_id:
            branches = Branch.objects.filter(account_id=account_id).values_list('id', flat=True)
            return Employee.objects.filter(branch_id__in=branches,status=job_type)

        else:
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
    serializer_class = BranchSerializer

    def get_queryset(self):
        account_id = self.request.session.get('account_id') 
        branch_id = self.request.session.get('branch_id') 
        if branch_id:
            return Branch.objects.get(id=branch_id)
            
        elif account_id:
           return Branch.objects.filter(account_id = account_id) 
            
        else:
            return Branch.objects.none()



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

        account_id = self.request.session.get('account_id') 
        branch_id = self.request.session.get('branch_id') 
        print("account_id",account_id)
        if branch_id and customer_type :
            return Customer.objects.filter(customer_type=customer_type,branch_id=branch_id)
            
        elif account_id and customer_type:
           branches = Branch.objects.filter(account_id = account_id).values_list('id',flat=True)
           return Customer.objects.filter(customer_type=customer_type,branch_id__in=branches) 
            
        else:
            return Customer.objects.none()
    


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
        
   
        expense_type = self.request.query_params.get("type")
        
        account_id = self.request.session.get('account_id') 
        branch_id = self.request.session.get('branch_id') 
        if branch_id and expense_type :
            return Expense.objects.filter(type=expense_type,branch_id=branch_id)
            
        elif account_id and expense_type:
           branches = Branch.objects.filter(account_id = account_id).values_list('id',flat=True)
           return Expense.objects.filter(type=expense_type,branch_id__in=branches) 
            
        else:
            return Expense.objects.none()



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
    queryset = Income.objects.all()
    serializer_class = AddIncomeSerializer
    lookup_field = "id"


class AddAdvance_amount(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Advance_amount.objects.all()
    serializer_class = AddAdvance_amountSerializer


class ListAdvance_amount(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddAdvance_amountSerializer
    def get_queryset(self):
        job_card_id = self.request.query_params.get("job_card_id")
        if job_card_id:
            return Advance_amount.objects.filter(job_card_id=job_card_id)


class DeleteAdvance_amount(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Advance_amount.objects.all()
    serializer_class = AddAdvance_amountSerializer
    lookup_field = "id"

class DashboardDatas(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filter = self.request.query_params.get("filter")
        now = timezone.now()
        if filter == "all":
            total_jobs = JobCard.objects.all().count()
            total_purchase = Expense.objects.filter(type=Expense.JOB).aggregate(total=Sum('total_cost'))['total'] or 0
            total_expense_other =  Expense.objects.filter(type=Expense.OTHER).aggregate(total=Sum('total_cost'))['total'] or 0
            expense_salary =   Expense.objects.filter(type=Expense.SALARY).aggregate(salary_total=Sum('salary'),other_total=Sum('other_expense'))
            total_expense_salary = (expense_salary['salary_total'] or 0) + (expense_salary['other_total'] or 0)
            total_expense = total_purchase + total_expense_other + total_expense_salary 
            income_job = Income.objects.filter(type=Income.JOB,date__year=now.year,date__month=now.month).aggregate(total=Sum('total_income'))['total'] or 0
            income_other = Income.objects.filter(type=Income.OTHER,date__year=now.year,date__month=now.month).aggregate(total=Sum('total_income'))['total'] or 0
            total_income = income_job + income_other


            total_purchase_month = Expense.objects.filter(type=Expense.JOB,date__year=now.year,date__month=now.month).aggregate(total=Sum('total_cost'))['total'] or 0
            total_expense_other_month =  Expense.objects.filter(type=Expense.OTHER,date__year=now.year,date__month=now.month).aggregate(total=Sum('total_cost'))['total'] or 0
            expense_salary_month =   Expense.objects.filter(type=Expense.SALARY,date__year=now.year,date__month=now.month).aggregate(salary_total=Sum('salary'),other_total=Sum('other_expense'))
            total_expense_salary_month = (expense_salary_month['salary_total'] or 0) + (expense_salary_month['other_total'] or 0)
            total_expense_month = total_purchase_month + total_expense_other_month + total_expense_salary_month

            total_balance = total_income - total_expense_month   
            total_values = {
            "total_jobs": total_jobs,
            "total_purchase":total_purchase,
            "total_expense":total_expense,
            "total_income":total_income,
            "total_balance":total_balance
        }
        return Response(total_values)



