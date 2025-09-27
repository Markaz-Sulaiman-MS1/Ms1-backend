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
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from datetime import date, timedelta
from django.db.models import Max
from django.utils import timezone
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from datetime import datetime
from django.db.models import FloatField
from django.shortcuts import get_object_or_404


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
            
            refresh['account_id'] = str(self.user.account.id) if self.user.account else None
            refresh['branch_id'] = str(self.user.branch.id) if self.user.branch else None
            refresh['team_id'] = str(self.user.team.id) if self.user.team else None
            # response.data["account_id"] = self.request.session.get("account_id")

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
         
         account_id = getattr(self.request.user, 'account_id', None) 
         branch_id = getattr(self.request.user, 'branch_id', None) 
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
        account_id = getattr(self.request.user, 'account_id', None) 
        branch_id = getattr(self.request.user, 'branch_id', None) 
        if branch_id:
            return JobCard.objects.filter(status=job_type,branch_id=branch_id)

        elif account_id:
            branches = Branch.objects.filter(account_id=account_id).values_list('id', flat=True)
            return JobCard.objects.filter(branch_id__in=branches,status=job_type)

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
        account_id = getattr(self.request.user, 'account_id', None) 
        branch_id = getattr(self.request.user, 'branch_id', None) 
        if branch_id:
            return Branch.objects.get(id=branch_id)
            
        elif account_id:
           return Branch.objects.filter(account_id = account_id) 
            
        else:
            return Branch.objects.none()



class ListJobType(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobTypeSerializer

    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None) 

        if account_id:
           return JobType.objects.filter(account_id = account_id)   
        else:
            return JobType.objects.none() 


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


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        # Attach custom claims to the user object
        user.account_id = validated_token.get('account_id')
        user.branch_id = validated_token.get('branch_id')
        user.team_id = validated_token.get('team_id')
        return user
    

class ListCustomers(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ListCustomerSerializer

    def get_queryset(self):                                               
        customer_type = self.request.query_params.get("customer_type")
        account_id = getattr(self.request.user, 'account_id', None)
        branch_id = getattr(self.request.user, 'branch_id', None)
        print("account_id",account_id)
            
        if account_id and customer_type:
           print("account_id222",account_id)
           
           return Customer.objects.filter(customer_type=customer_type,account_id=account_id) 
            
        raise ValidationError({"message": "No session data","account":account_id})
    


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
        
        account_id = getattr(self.request.user, 'account_id', None) 
        branch_id = self.request.query_params.get("branch")              
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
        account_id = getattr(self.request.user, 'account_id', None)
        branch_id = self.request.query_params.get("branch")
        type = self.request.query_params.get("type")
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")


        if branch_id and type:
            if from_date and to_date:        
                return Income.objects.filter(type=type,branch_id=branch_id,created_at__date__gte=from_date,created_at__date__lte=to_date)
            else:
                return Income.objects.filter(type=type,branch_id=branch_id)

        elif account_id and type:
            branches = Branch.objects.filter(account_id = account_id).values_list('id',flat=True)

            if from_date and to_date:        
                return Income.objects.filter(type=type,branch_id__in=branches,created_at__date__gte=from_date,created_at__date__lte=to_date)   
            else:
                return Income.objects.filter(type=type,branch_id__in=branches)
        else:
            return Income.objects.none()





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


class CreateBranch(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class UpdateBranch(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = "id"


class DeleteBranch(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = "id"

class CreateJobType(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class UpdateJobType(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    lookup_field = "id"


class DeleteJobType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    lookup_field = "id"


class CreateTeam(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class ListTeam(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer



class TotalIncome(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        account_id = getattr(self.request.user, 'account_id', None) 
        branch_id = request.query_params.get("branch")
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date") 
        total_sum = 0
        total_jobs_sum = 0
        total_other_sum = 0

        
        if branch_id :
            if from_date and to_date:        
                total =  Income.objects.filter(branch_id=branch_id,created_at__date__gte=from_date,created_at__date__lte=to_date).aggregate(total_sum=Sum('total_income'))
                total_jobs =  Income.objects.filter(type=Income.JOB,branch_id=branch_id,created_at__date__gte=from_date,created_at__date__lte=to_date).aggregate(total_sum=Sum('total_income'))
                total_other =  Income.objects.filter(type=Income.OTHER,branch_id=branch_id,created_at__date__gte=from_date,created_at__date__lte=to_date).aggregate(total_sum=Sum('total_income'))
                total_sum = total['total_sum'] or 0
                total_jobs_sum = total_jobs['total_sum'] or 0
                total_other_sum = total_other['total_sum'] or 0
                                  
            else:
                total = Income.objects.filter(branch_id=branch_id).aggregate(total_sum=Sum('total_income'))
                total_jobs =  Income.objects.filter(type=Income.JOB,branch_id=branch_id).aggregate(total_sum=Sum('total_income'))
                total_other =  Income.objects.filter(type=Income.OTHER,branch_id=branch_id).aggregate(total_sum=Sum('total_income'))
                total_sum = total['total_sum'] or 0
                total_jobs_sum = total_jobs['total_sum'] or 0
                total_other_sum = total_other['total_sum'] or 0

            total = {
                "total_sum":total_sum,
                "total_jobs_sum":total_jobs_sum,
                "total_other_sum":total_other_sum
            }
            
            return Response(total)
            

        elif account_id :
            branches = Branch.objects.filter(account_id = account_id).values_list('id',flat=True)

            if from_date and to_date:        
                total = Income.objects.filter(branch_id__in=branches,created_at__date__gte=from_date,created_at__date__lte=to_date).aggregate(total_sum=Sum('total_income'))
                total_jobs =  Income.objects.filter(type=Income.JOB,branch_id__in=branches,created_at__date__gte=from_date,created_at__date__lte=to_date).aggregate(total_sum=Sum('total_income'))
                total_other =  Income.objects.filter(type=Income.OTHER,branch_id__in=branches,created_at__date__gte=from_date,created_at__date__lte=to_date).aggregate(total_sum=Sum('total_income'))
                total_sum = total['total_sum'] or 0
                total_jobs_sum = total_jobs['total_sum'] or 0
                total_other_sum = total_other['total_sum'] or 0

            else:
                total = Income.objects.filter(branch_id__in=branches).aggregate(total_sum=Sum('total_income'))
                total_jobs = Income.objects.filter(type=Income.JOB,branch_id__in=branches).aggregate(total_sum=Sum('total_income'))
                total_other = Income.objects.filter(type=Income.OTHER,branch_id__in=branches).aggregate(total_sum=Sum('total_income'))

                total_sum = total['total_sum'] or 0
                total_jobs_sum = total_jobs['total_sum'] or 0
                total_other_sum = total_other['total_sum'] or 0

            total = {
                "total_sum":total_sum,
                "total_jobs_sum":total_jobs_sum,
                "total_other_sum":total_other_sum
            }
            
            return Response(total)
            
            
        else:
            return Income.objects.none()
        




class TotalExpense(APIView):
    permission_classes = [IsAuthenticated]

    def parse_date(self, date_str):

        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    def get(self, request):
        account_id = getattr(request.user, "account_id", None)
        branch_id = request.query_params.get("branch")

        # Parse dates safely
        from_date = self.parse_date(request.query_params.get("from_date"))
        to_date = self.parse_date(request.query_params.get("to_date"))

        # Build date filters if valid
        date_filter = {}
        if from_date:
            date_filter["created_at__date__gte"] = from_date
        if to_date:
            date_filter["created_at__date__lte"] = to_date

        # Determine branches to filter
        if branch_id:
            branches = [branch_id]
        elif account_id:
            branches = Branch.objects.filter(account_id=account_id).values_list("id", flat=True)
        else:
            return Response([])  # No branch or account -> return empty

        # Base queryset
        base_qs = Expense.objects.filter(branch_id__in=branches, **date_filter)

        # Aggregate totals safely using Coalesce
        total_sum = base_qs.aggregate(
          total_sum=Sum(
        Coalesce(F("total_cost"), Value(0, output_field=FloatField()))
        + Coalesce(F("salary"), Value(0, output_field=FloatField()))
        + Coalesce(F("other_expense"), Value(0, output_field=FloatField())),
        output_field=FloatField()
    )
        )["total_sum"] or 0

        # Aggregate individual types
        total_purchase = base_qs.filter(type=Expense.JOB).aggregate(total_sum=Sum("total_cost"))["total_sum"] or 0
        total_salary = base_qs.filter(type=Expense.SALARY).aggregate(total_sum=Sum(Coalesce(F("salary"), Value(0, output_field=FloatField()))+ Coalesce(F("other_expense"), Value(0, output_field=FloatField())),output_field=FloatField()))["total_sum"] or 0
        total_overtime = base_qs.filter(type=Expense.OVERTIME).aggregate(total_sum=Sum("total_cost"))["total_sum"] or 0
        total_other = base_qs.filter(type=Expense.OTHER).aggregate(total_sum=Sum("total_cost"))["total_sum"] or 0

        result = {
            "total_overtime": total_overtime,
            "total_purchase": total_purchase,
            "total_salary": total_salary,
            "total_other": total_other,
            "total_sum": total_sum,
        }

        return Response(result)
        

class CreateDeposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get("amount")
            branch = request.data.get("branch")
            deposit_type = request.data.get("deposit_type")
            date = request.data.get("date")
            description = request.data.get("description")

            if not amount or not branch or not deposit_type:
                return Response(
                    {"error": "amount, branch and deposit_type are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Ensure amount is numeric
            try:
                amount = float(amount)
            except ValueError:
                return Response(
                    {"error": "Amount must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if deposit_type == "Cash":
                balance, created = Balance.objects.get_or_create(
                    branch_id=branch,
                    defaults={'cash_balance': amount}
                )
                
                if not created:
                    balance.cash_balance += amount
                    balance.save()

                transaction = RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.DEPOSIT,
                    description=description,
                    payment_type=RecentTransaction.CASH,
                    amount=amount,
                    balance_cash=balance.cash_balance,
                    balance_bank=balance.bank_balance,
                    branch_id=branch,
                    date=date
                )
            elif deposit_type == "Bank":
                balance, created = Balance.objects.get_or_create(
                    branch_id=branch,
                    defaults={'bank_balance': amount}
                )
                
                if not created:
                    balance.bank_balance += amount
                    balance.save()

                transaction = RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.DEPOSIT,
                    description=description,
                    payment_type=RecentTransaction.BANK,
                    amount=amount,
                    balance_cash=balance.cash_balance,
                    balance_bank=balance.bank_balance,
                    branch_id=branch,
                    date=date
                )
            else:
                return Response(
                    {"error": "Invalid deposit_type. Must be 'Cash' or 'Bank'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "message": "Deposit created successfully",
                    "transaction_id": transaction.id,
                    "balance_cash": balance.cash_balance,
                    "balance_bank": balance.bank_balance
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class CreateWithdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get("amount")
            branch = request.data.get("branch")
            deposit_type = request.data.get("deposit_type")
            date = request.data.get("date")
            description = request.data.get("description")

            try:
                amount = float(amount)
            except ValueError:
                return Response(
                    {"error": "Amount must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )


            if deposit_type == "Cash":
                balance = Balance.objects.get(branch_id=branch)
                if balance:
                    balance.cash_balance -= amount
                    balance.save()

                RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.WITHDRAWAL,
                    description=description,
                    payment_type=RecentTransaction.CASH,
                    amount=amount,
                    balance_cash=balance.cash_balance,
                    balance_bank=balance.bank_balance,
                    branch_id=branch,
                    date=date

                )

            elif deposit_type == "Bank":
                balance = Balance.objects.get(branch_id=branch)
                if balance:
                    balance.bank_balance -= amount
                    balance.save()

                RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.WITHDRAWAL,
                    description=description,
                    payment_type=RecentTransaction.BANK,
                    amount=amount,
                    balance_cash=balance.cash_balance,
                    balance_bank=balance.bank_balance,
                    branch_id=branch,
                    date=date
                )

            return Response(
                {"message": "Withdrawal successful"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 


class ListBalance(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer  # <- only used if you actually serialize balances

    def list(self, request, *args, **kwargs):
        branch = request.query_params.get("branch")
        balance = Balance.objects.filter(branch_id=branch).first()

        if not balance:
            current_balances = {
            "cash_balance": 0,
            "bank_balance": 0,
            }
            return Response(current_balances)
             

        current_balances = {
            "cash_balance": balance.cash_balance,
            "bank_balance": balance.bank_balance,
        }
        return Response(current_balances)




class List_Transactions(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionsSerializer
    def get_queryset(self):
        branch = self.request.query_params.get("branch")
        transactions = RecentTransaction.objects.filter(branch_id=branch)
        return transactions

    


class LastDayBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        branch = request.query_params.get("branch")
        try:
            today = timezone.localdate()

            # Find the last transaction date before today
            last_txn_date = (RecentTransaction.objects
                .filter(created_at__lt=today, branch_id=branch)
                .aggregate(last_date=Max("created_at"))["last_date"])

            if not last_txn_date:
                return Response({"message": "No past transactions found"}, status=404)

            # Get the latest transaction of that day
            last_txn = (RecentTransaction.objects
                .filter(created_at=last_txn_date, branch_id=branch)
                .order_by("-created_at")
                .first())

            data = {
                "date": str(last_txn_date),
                "balance_cash": last_txn.balance_cash,
                "balance_bank": last_txn.balance_bank,
                "all_balance": last_txn.balance_cash + last_txn.balance_bank
            }
            return Response(data, status=200)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500
            )

class CreditOutstandingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        branch = request.query_params.get("branch")
        try:
            credit_jobcards = JobCard.objects.filter(status=JobCard.CREDIT,branch_id=branch)

            total_credit = BillAmount.objects.filter(
                job_card__in=credit_jobcards
            ).aggregate(total=Sum("amount"))["total"] or 0

            return Response(
                {"total_credit_outstanding": total_credit},
                status=200
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500) 
        

class UserCreateAPIView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEditAPIView(APIView):
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User partially updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class GetDepartment(APIView):
    def get(self, request):
        role = request.query_params.get("role")
        if not role:
            return Response({"error": "role query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        departments = Designation.objects.filter(role_id=role)
        serializer = DesignationSerializer(departments, many=True)
        return Response({"departments": serializer.data}, status=status.HTTP_200_OK)
    

class ListRole(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
