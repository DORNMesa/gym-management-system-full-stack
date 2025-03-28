from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import datetime

from user.models import User
from schedule.models import Schedule
from attendance.models import Attendance
from transaction.models import Credit
# Create your views here.
def index(request):
    employees = User.objects.filter(is_employee=True)
    schedules = Schedule.objects.filter(name='stuff')
    
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        nid = request.POST.get("nid")
        gender = request.POST.get("gender")
        salary = request.POST.get("salary")
        address = request.POST.get("address")
        password = request.POST.get("password")
        schedules_res = request.POST.getlist("schedule")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect("/user/")

        # Check if phone number already exists
        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists. Please use a different phone number.")
            return redirect("/user/")

        try:
            lastId = User.objects.last().id if User.objects.exists() else 0

            user = User.objects.create(
                username=username,
                name=name,
                phone=phone,
                dob=dob,
                nid=nid,
                gender=gender,
                salary=salary,
                address=address,
                password=make_password(password),
                emp_id="FKE-" + str(lastId + 1),
                join_date=datetime.now(),
                is_employee=True,
                is_manager=False
            )

            for schedule in schedules_res:
                user.schedules.add(schedule)

            messages.success(request, "Employee added successfully")
            return redirect("/user/")
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return redirect("/user/")

    context = {
        'employees': employees,
        'schedules': schedules
    }
    return render(request, 'user/index.html', context)

def edit(request,pk):
    employee = User.objects.get(id = pk)
    schedules = Schedule.objects.filter(name = 'stuff')
    salaries = Credit.objects.filter(employee = employee)

    current_month = datetime.now().month
    current_year = datetime.now().year

    # Query the income data for the current month
    attendance = Attendance.objects.filter(date__month=current_month, date__year=current_year,employee=employee)


    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        nid = request.POST.get("nid")
        salary = request.POST.get("salary")
        address = request.POST.get("address")
        password = request.POST.get("password")
        schedules_res = request.POST.getlist("schedule")

        employee.name = name
        employee.phone = phone
        employee.salary = salary
        employee.nid = nid
        employee.address = address

        if password != "":
            employee.password = make_password(password)
            
        employee.save()

        employee.schedules.clear()
        for schedule in schedules_res:
            employee.schedules.add(schedule)

    context = {
        'employee': employee,
        'schedules':schedules,
        'attendance':attendance,
        'salaries':salaries
    }
    return render(request,"user/edit.html",context)

def attendance(request,pk,id):
    try:
        employee = User.objects.get(id = pk)
        attendance = Attendance.objects.get(employee = employee, id = id)
        if attendance.attendance:
            attendance.attendance = False
        else:
            attendance.attendance = True
        attendance.save()
    except:
        pass
    return redirect(f"/user/edit/{pk}")

def deactivate(request,pk):
    employee = User.objects.get(id = pk)
    employee.is_active = False
    employee.save()
    return redirect("/user/")

def active(request,pk):
    employee = User.objects.get(id = pk)
    employee.is_active = True
    employee.save()
    return redirect("/user/")

def delete(request,pk):
    User.objects.get(id = pk).delete()
    return redirect("/user/")
