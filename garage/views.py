from decimal import Decimal
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
from datetime import datetime, time
from django.db.models import FloatField
from django.shortcuts import get_object_or_404
from zoneinfo import ZoneInfo 
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import date
from num2words import num2words
from django.templatetags.static import static
import os
from django.conf import settings
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
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")              
        if branch_id and expense_type :
            if from_date and to_date:
                from_dt = parse_datetime(from_date)
                to_dt = parse_datetime(to_date)
                return Expense.objects.filter(type=expense_type,branch_id=branch_id,  created_at__range=(from_dt, to_dt))
            else: 
                return Expense.objects.filter(type=expense_type,branch_id=branch_id)
            
        elif account_id and expense_type:
           branches = Branch.objects.filter(account_id = account_id).values_list('id',flat=True)
           if from_date and to_date:
                from_dt = parse_datetime(from_date)
                to_dt = parse_datetime(to_date)
                return Expense.objects.filter(type=expense_type,branch_id__in=branches,created_at__range=(from_dt, to_dt))
           else:
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
                from_dt = parse_datetime(from_date)
                to_dt = parse_datetime(to_date)
        
                return Income.objects.filter(type=type,branch_id=branch_id,created_at__range=(from_dt, to_dt))
            else:
                return Income.objects.filter(type=type,branch_id=branch_id)

        elif account_id and type:
            branches = Branch.objects.filter(account_id = account_id).values_list('id',flat=True)

            if from_date and to_date: 
                from_dt = parse_datetime(from_date)
                to_dt = parse_datetime(to_date)
                return Income.objects.filter(type=type,branch_id__in=branches,created_at__range=(from_dt, to_dt))   
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
                from_dt = parse_datetime(from_date)
                to_dt = parse_datetime(to_date)
                    
                total =  Income.objects.filter(branch_id=branch_id,created_at__range=(from_dt, to_dt)).aggregate(total_sum=Sum('total_income'))
                total_jobs =  Income.objects.filter(type=Income.JOB,branch_id=branch_id,created_at__date__gte=from_dt,created_at__date__lte=to_dt).aggregate(total_sum=Sum('total_income'))
                total_other =  Income.objects.filter(type=Income.OTHER,branch_id=branch_id,created_at__date__gte=from_dt,created_at__date__lte=to_dt).aggregate(total_sum=Sum('total_income'))
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
                from_dt = parse_datetime(from_date)
                to_dt = parse_datetime(to_date)      
                total = Income.objects.filter(branch_id__in=branches,created_at__range=(from_dt, to_dt)).aggregate(total_sum=Sum('total_income'))
                total_jobs =  Income.objects.filter(type=Income.JOB,branch_id__in=branches,created_at__date__gte=from_dt,created_at__date__lte=to_dt).aggregate(total_sum=Sum('total_income'))
                total_other =  Income.objects.filter(type=Income.OTHER,branch_id__in=branches,created_at__date__gte=from_dt,created_at__date__lte=to_dt).aggregate(total_sum=Sum('total_income'))
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
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")

        # Build date filters if valid
        date_filter = {}
        if from_date:
            from_dt = parse_datetime(from_date)
            date_filter["created_at__gte"] = from_dt
        if to_date:
            to_dt = parse_datetime(to_date) 
            date_filter["created_at__lte"] = to_dt

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

            branch = Branch.objects.select_related("timezone").get(id=branch)
            if not branch.timezone or not branch.timezone.name:
                return Response({"error": "Branch has no timezone configured"}, status=400)
            
            branch_tz = ZoneInfo(branch.timezone.name)
            today = timezone.now().astimezone(branch_tz).date()
    

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
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")  
        try:
            if from_date and to_date:
                from_dt = parse_datetime(from_date)
                to_dt = parse_datetime(to_date)
                credit_jobcards = JobCard.objects.filter(status=JobCard.CREDIT,branch_id=branch,created_at__range=(from_dt, to_dt))
            else:
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
        serializer = UsersCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEditAPIView(APIView):
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UsersCreateSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UsersCreateSerializer(user, data=request.data, partial=True)
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


class ListUsers(generics.ListAPIView):

    serializer_class = UsersSerializer
    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None) 
        branch_id = getattr(self.request.user, 'branch_id', None) 
        if branch_id:
            return User.objects.filter(branch_id=branch_id)
            
        elif account_id:
           return User.objects.filter(account_id=account_id)         
            
        else:
            return User.objects.none()

    
class ListTimezones(generics.ListAPIView):
    serializer_class = TimeZoneSerilaizer
    queryset = TimeZone.objects.all()
    




class CreateBrand(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            account_id = getattr(self.request.user, 'account_id', None)
            if not account_id:
                return Response({"error": "Account not found for user"}, status=400)

            name = request.data.get("name")
            description = request.data.get("description")

            if not name:
                return Response({"error": "Name is required"}, status=400)

            brand = Brand.objects.create(
                name=name,
                description=description,
                account_id=account_id 
            )

            return Response(
                {"message": "Brand created successfully", "brand_id": brand.id},
                status=201
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class ListBrand(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = BrandSerializer
    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None) 
            
        if account_id:
           return Brand.objects.filter(account_id=account_id)         
            
        else:
            return Brand.objects.none()





class CreateCategory(APIView):
    def post(self, request):
        try:
            account_id = getattr(self.request.user, 'account_id', None)
            if not account_id:
                return Response({"error": "Account not found for user"}, status=400)

            name = request.data.get("name")
            description = request.data.get("description")

            if not name:
                return Response({"error": "Name is required"}, status=400)

            category = Category.objects.create(
                name=name,
                description=description,
                account_id=account_id 
            )

            return Response(
                {"message": "Category created successfully", "category_id": category.id},
                status=201
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        


class ListCategory(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None) 
            
        if account_id:
           return Category.objects.filter(account_id=account_id)         
            
        else:
            return Category.objects.none()

class CreateVendor(APIView):
    def post(self, request):
        try:
            account_id = getattr(self.request.user, 'account_id', None)
            if not account_id:
                return Response({"error": "Account not found for user"}, status=400)

            name = request.data.get("name")
            description = request.data.get("description")

            if not name:
                return Response({"error": "Name is required"}, status=400)

            vendor = Vendor.objects.create(
                name=name,
                description=description,
                account_id=account_id 
            )

            return Response(
                {"message": "Category created successfully", "vendor_id": vendor.id},
                status=201
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class ListVendor(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer
    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None) 
            
        if account_id:
           return Vendor.objects.filter(account_id=account_id)         
            
        else:
            return Vendor.objects.none()
        



class CreateProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        account_id = getattr(self.request.user, 'account_id', None)
        if not account_id:
            raise serializers.ValidationError("Account not found for user.")
        serializer.save(account_id=account_id)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None)
        return Product.objects.filter(account_id=account_id)
    

class CreateSellPack(generics.CreateAPIView):
    queryset = SellPack.objects.all()
    serializer_class = SellPackSerializer
    permission_classes = [IsAuthenticated]


class CreateSellPart(generics.CreateAPIView):
    queryset = SellPart.objects.all()
    serializer_class = SellPartSerializer
    permission_classes = [IsAuthenticated]


class ListSellPack(generics.ListAPIView):
    serializer_class = SellPackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.request.query_params.get("product") 
            
        if product_id:
           return SellPack.objects.filter(product_id=product_id)         
            
        else:
            return SellPart.objects.none()
        

class ListSellPart(generics.ListAPIView):
    serializer_class = SellPackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.request.query_params.get("product") 
            
        if product_id:
           return SellPart.objects.filter(product_id=product_id)         
            
        else:
            return SellPart.objects.none()
        


class AddPurchaseAPIView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class ListPurchase(APIView):
    def get(self, request):
        branch_id =  getattr(self.request.user, 'branch_id', None)
        account_id = getattr(self.request.user, 'account_id', None) 
        status_filter = request.query_params.get("status", None)

        if status_filter and account_id :
            purchases = Purchase.objects.filter(purchase_type=status_filter,is_deleted = False,account_id=account_id)
        elif status_filter and branch_id:
            purchases = Purchase.objects.filter(purchase_type=status_filter,is_deleted = False,branch_id=branch_id)
        else:
            purchases = Purchase.objects.none


        serializer = PurchaseListSerializer(purchases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EditPurchase(APIView):
    def patch(self, request, purchase_id):
        try:
            purchase = Purchase.objects.get(id=purchase_id)
        except Purchase.DoesNotExist:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditPurchaseSerializer(purchase, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Purchase updated successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class DeletePurchase(APIView):
    def delete(self, request, item_id):
        try:
            item = Purchase.objects.get(id=item_id)
        except ProductItem.DoesNotExist:
            return Response({"error": "Purchase item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.is_deleted = True
        item.save()

        return Response({"message": "Purchase item deleted successfully"}, status=status.HTTP_200_OK)

class AddPurchaseItems(APIView):
    def post(self, request):
        purchase_id = request.data.get("purchase_id")
        items = request.data.get("items")

        if not purchase_id or not items:
            return Response({"error": "purchase_id and items are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase = Purchase.objects.get(id=purchase_id)
        except Purchase.DoesNotExist:
            return Response({"error": "Invalid purchase_id"}, status=status.HTTP_404_NOT_FOUND)

        created_items = []

        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            amount = item.get("amount")

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": f"Invalid product_id: {product_id}"}, status=status.HTTP_404_NOT_FOUND)

            p_item = ProductItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=quantity,
                amount=float(quantity) * float(product.cost_price)
            )
            created_items.append(p_item.id)

        return Response({
            "message": "Items added successfully",
            "count": len(created_items),
            "item_ids": created_items
        }, status=status.HTTP_201_CREATED)


class EditPurchaseItems(APIView):
    def patch(self, request, item_id):
        try:
            item = ProductItem.objects.get(id=item_id)
        except ProductItem.DoesNotExist:
            return Response({"error": "Purchase item not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        amount = request.data.get("amount")

        if quantity is not None:
            item.quantity = quantity
        if amount is not None:
            item.amount = amount

        item.save()

        return Response({
            "message": "Purchase item updated successfully",
            "item_id": str(item.id),
            "data": {
                "product": str(item.product.id),
                "quantity": item.quantity,
                "amount": item.amount
            }
        }, status=status.HTTP_200_OK)
    


class ListPurchaseItems(APIView):
    def get(self, request):
        purchase_id = request.query_params.get("purchase_id", None)

        if purchase_id:
            items = ProductItem.objects.filter(purchase__id=purchase_id,is_deleted=False)
        else:
            items = ProductItem.objects.none

        serializer = ProductItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class DeletePurchaseItem(APIView):
    def delete(self, request, item_id):
        try:
            item = ProductItem.objects.get(id=item_id)
        except ProductItem.DoesNotExist:
            return Response({"error": "Purchase item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.is_deleted = True
        item.save()

        return Response({"message": "Purchase item deleted successfully"}, status=status.HTTP_200_OK)
    


class UpdatePurchaseStatus(APIView):
    def patch(self,request,item_id):
        status = request.data.get("status")
        cash_type = request.data.get("cash_type")
        try:
            purchase = Purchase.objects.get(id=item_id)
        except Purchase.DoesNotExist:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)
        
        purchase.purchase_type = status
        purchase.save()

        if purchase.purchase_type == Purchase.COMPLETED:

            total = ProductItem.objects.filter(purchase=purchase, is_deleted=False).aggregate(total_amount=Sum('amount'))['total_amount']

            expense = Expense.objects.create(
                payment_type=cash_type,
                type=Expense.PURCHASE,
                name=f"Purchase {purchase.po_nmbr}",
                description = f"Purchase done for {total}",
                total_cost = total,
                date=timezone.now().date(),
                other_expense =  total,
                branch=purchase.branch,
            )

            if cash_type == JobCard.CASH:
                                    
                balance, created = Balance.objects.get_or_create(
                branch=purchase.branch,
                defaults={
                    'cash_balance': total,
                }
                )
                if not created:
                    
                    balance.cash_balance -= total
                    balance.save()

                RecentTransaction.objects.create(
                        transaction_type=RecentTransaction.EXPENSE,
                        description = f"{expense.type} expense transferred as cash",
                        payment_type = expense.payment_type,
                        amount = total,
                        balance_cash = balance.cash_balance,
                        balance_bank = balance.bank_balance,
                        branch_id=expense.branch.id
                )

            elif cash_type == JobCard.BANK:
                balance, created = Balance.objects.get_or_create(
                branch=purchase.branch,
                defaults={
                    'bank_balance': total,
                }
                )
                        
                if not created:
                    balance.bank_balance -= total
                    balance.save()

                RecentTransaction.objects.create(
                        transaction_type=RecentTransaction.EXPENSE,
                        description = f"{expense.type} expense transferred to bank",
                        payment_type = expense.payment_type,
                        amount = total,
                        balance_cash = balance.cash_balance,
                        balance_bank = balance.bank_balance,
                        branch_id=expense.branch.id
                        
                 )


class CreateBatch(APIView):
    def post(self, request):
        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Batch created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED 
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UpdateBatch(APIView):
    def patch(self, request, batch_id):
        try:
            batch = Batch.objects.get(id=batch_id, is_deleted=False)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BatchSerializer(batch, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Batch updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LabourCreateAPIView(generics.CreateAPIView):
    serializer_class = LabourSerializer

    def perform_create(self, serializer):
        account_id = getattr(self.request.user, 'account_id', None)
        if not account_id:
            raise serializers.ValidationError("Account not found for user.")
        serializer.save(account_id=account_id)


class LabourListAPIView(generics.ListAPIView):
    serializer_class = LabourSerializer

    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None)
        if not account_id:
            raise serializers.ValidationError("Account not found for user.")
        return Labour.objects.filter(
            account_id=account_id,
            is_deleted=False
        )
    
class LabourUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LabourSerializer
    lookup_field = "id"

    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None)
        return Labour.objects.filter(
            account_id=account_id,
            is_deleted=False
        )
    

class LabourSoftDeleteAPIView(generics.DestroyAPIView):
    lookup_field = "id"

    def get_queryset(self):
        account_id = getattr(self.request.user, 'account_id', None)
        return Labour.objects.filter(
            account_id=account_id,
            is_deleted=False
        )

    def delete(self, request, *args, **kwargs):
        labour = self.get_object()
        labour.is_deleted = True
        labour.save()
        return Response(
            {"message": "Labour deleted successfully"},
            status=status.HTTP_200_OK
        )






def amount_to_words(amount):
    """
    Convert numeric amount to words in Riyal format.
    Example: 1380.50 -> ONE THOUSAND THREE HUNDRED EIGHTY RIYAL AND FIFTY HALALA ONLY
    """
    amount = round(float(amount), 2)
    integer_part = int(amount)
    decimal_part = int(round((amount - integer_part) * 100))

    words = num2words(integer_part, lang="en").upper() + " RIYAL"

    if decimal_part > 0:
        words += " AND " + num2words(decimal_part, lang="en").upper() + " HALALA"

    return words + " ONLY"


def jobcard_quotation_pdf(request, jobcard_id):
    jobcard = get_object_or_404(JobCard, id=jobcard_id)

    spare_parts = SpareParts.objects.filter(job_card=jobcard)
    labours = jobcard.labour.all()

    # ---------- CALCULATIONS ----------
    spare_rows = []
    spare_total = Decimal("0.00")

    for idx, sp in enumerate(spare_parts, start=1):
        qty = sp.quantity or 1
        cost = Decimal(sp.cost or 0)
        amount = qty * cost

        spare_total += amount

        spare_rows.append({
            "no": idx,
            "name": sp.name,
            "price": f"{cost:.2f}",
            "qty": qty,
            "amount": f"{amount:.2f}",
        })

    labour_rows = []
    labour_total = Decimal("0.00")

    for idx, lb in enumerate(labours, start=len(spare_rows) + 1):
        rate = Decimal(lb.rate or 0)
        labour_total += rate

        labour_rows.append({
            "no": idx,
            "description": lb.description or lb.name,
            "price": f"{rate:.2f}",
            "qty": 1,
            "amount": f"{rate:.2f}",
        })

    subtotal = spare_total + labour_total
    discount = Decimal("0.00")
    vat = subtotal * Decimal("0.15")
    grand_total = subtotal + vat - discount
    
    # logo_url = request.build_absolute_uri(
    #     static("image/logo-color.png")
    # )

    logo_path = os.path.join(
    settings.BASE_DIR,
    "static",
    "images",
    "msi-logo.png"
)

    context = {
        # Header
        "quotation_number": f"SO-{str(jobcard.id)[:6].upper()}",
        "date": date.today().strftime("%d/%m/%Y"),

        # Customer & Vehicle
        "customer_name": jobcard.customer.name if jobcard.customer else "",
        "customer_phone": jobcard.customer.phn_nmbr or "",
        "vehicle_number": jobcard.vehicle_nmbr or "",
        "vehicle_model": jobcard.make_and_model or "",

        # Tables
        "spare_rows": spare_rows,
        "labour_rows": labour_rows,

        # Totals
        "spare_total": f"{spare_total:.2f}",
        "labour_total": f"{labour_total:.2f}",
        "subtotal": f"{subtotal:.2f}",
        "discount": f"{discount:.2f}",
        "vat": f"{vat:.2f}",
        "grand_total": f"{grand_total:.2f}",

        # Amount in words (simple)
        "amount_words": amount_to_words(grand_total),
    }
    context["logo_url"] = f"file:///{logo_path.replace(os.sep, '/')}"

    html_string = render_to_string(
        "quotation/jobcard_quotation.html",
        context
    )

    pdf = HTML(string=html_string,base_url=request.build_absolute_uri("/")).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Quotation_{jobcard.id}.pdf"'
    )

    return response

class UnitListAPIView(generics.ListAPIView):
    queryset = Units.objects.all().order_by("name")
    serializer_class = UnitSerializer



class DeleteJobCard(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobCard.objects.all()
    serializer_class = AddJobCardSerializer
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        job_card = self.get_object()

 
        if job_card.status != "Draft":
            return Response(
                {
                    "error": "Only Job Cards in Draft status can be deleted."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        job_card.delete()
        return Response(
            {"message": "Job Card deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
