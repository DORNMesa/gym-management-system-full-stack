from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from decimal import Decimal, InvalidOperation

from .models import Credit,Debit
from user.models import User
from coach.models import Coach
from user.models import MetaData


# Create your views here.
def index(request):
    debits = Debit.objects.all().order_by("-date")
    credits = Credit.objects.all().order_by("-date")

    employees = User.objects.filter(due__gt = 0)
    coaches = Coach.objects.filter(due__gt = 0)

    if request.method == "POST":
        searchCoach = request.POST.get("searchCoach")
        searchEmp = request.POST.get("searchEmp")

        if searchCoach != "":
            coaches = Coach.objects.filter(Q(name__icontains=searchCoach) | Q(coachId__icontains=searchCoach))

        if searchEmp != "":
            employees = User.objects.filter(Q(name__icontains=searchEmp) | Q(emp_id__icontains=searchEmp))

    context = {
        'debits':debits,
        'credits':credits,
        'employees':employees,
        'coaches':coaches,
    }
    return render(request,'transaction/index.html',context)


def payE(request, pk):
    employee = User.objects.get(id=pk)
    
    if request.method == "POST":
        try:
            amount = request.POST.get("amount", "0")
            # Safer conversion with decimal handling
            amount_decimal = Decimal(amount).quantize(Decimal('0.01'))
            amount_int = int(amount_decimal)

            if amount_int <= 0:
                messages.error(request, "Amount must be positive")
                return redirect("/transaction/")

            timestamp = int(datetime.now().timestamp())
            employee.due -= amount_int
            employee.save()

            Credit.objects.create(
                trxId='FK-TRX-' + str(timestamp),
                reason='salary_employee',
                amount=amount_int,
                date=datetime.now(),
                is_employee=True,
                employee=employee
            )
            meta = MetaData.objects.last()
            meta.funds -= amount_int
            meta.save()

            return redirect("/transaction/")
        except (ValueError, InvalidOperation):
            messages.error(request, "Invalid amount format")
            
    context = {
        'employee':employee
    }
    return render(request,'transaction/payEmployee.html',context)

def payC(request,pk):
    coach = Coach.objects.get(id = pk)
    
    if request.method == "POST":
        amount = request.POST.get("amount")

        timestamp = int(datetime.now().timestamp())
        coach.due -= int(amount)

        coach.save()

        Credit.objects.create(
            trxId = 'FK-TRX-' + str(timestamp),
            reason = 'salary_coach',
            amount = int(amount),
            date = datetime.now(),
            is_coach = True,
            coach = coach
        )
        meta = MetaData.objects.last()
        meta.funds -= int(amount)
        meta.save()
        
        return redirect("/transaction/")
    context = {
        'coach':coach
    }
    return render(request,'transaction/payCoach.html',context)
