from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib import messages

from .models import Equipment,EquipmentType,EquipmentActivityTrack
from user.models import MetaData
from transaction.models import Credit
from member.models import Member
# Create your views here.
def index(request):
    eqs = Equipment.objects.all()
    eqTypes = EquipmentType.objects.all()
    eqActivities = EquipmentActivityTrack.objects.all()

    meta = MetaData.objects.last()
    if request.method == "POST":
        name = request.POST.get("name")
        brand = request.POST.get("brand")
        serial = request.POST.get("serial")
        price = request.POST.get("price")

        eqTypes_res = request.POST.getlist("eqType")


        eq = Equipment.objects.create(
            name = name,
            brand = brand,
            serial = serial,
            price = price,
            maintenanceDate = datetime.now()
        )
        for eqT in eqTypes_res:
            eq.equipmentType.add(eqT)
        
        timestamp = int(datetime.now().timestamp())

        costCondition = "store"
        
        if costCondition == "store":
            Credit.objects.create(
                trxId = 'FK-TRX-' + str(timestamp),
                reason = 'buy_equipment',
                amount = int(price),
                date = datetime.now(),
                is_equipment = True,
                equipment = eq
            )
            meta.funds -= int(price)
            meta.save()
        
    context = {
        'eqs':eqs,
        'eqTypes':eqTypes,
        'eqActivities':eqActivities
    }
    return render(request,'equipment/index.html',context)

def edit(request,pk):
    eq = Equipment.objects.get(id = pk)
    eqTypes = EquipmentType.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        brand = request.POST.get("brand")
        eqTypes_res = request.POST.getlist("eqType")

        eq.name = name
        eq.brand = brand

            
        eq.save()

        eq.equipmentType.clear()
        for eqT in eqTypes_res:
            eq.equipmentType.add(eqT)

    context = {
        'eq':eq,
        'eqTypes':eqTypes
    }
    return render(request,"equipment/edit.html",context)

def validateBookingTime(start_time, end_time):
    now = datetime.now()
    if start_time < now:
        return False, "Cannot book for past time"
    if end_time <= start_time:
        return False, "End time must be after start time"
    if (end_time - start_time).total_seconds() > 7200:  # 2 hours max
        return False, "Maximum booking duration is 2 hours"
    return True, ""

def activity(request):
    eqs = Equipment.objects.filter(is_available = True).order_by("-id")
    eqActivities = EquipmentActivityTrack.objects.all().order_by("start_time")[:5]
    members = Member.objects.filter(status=True).order_by("-id")



    if request.method == "POST":
        search = request.POST.get("search")
        eqs = Equipment.objects.filter(Q(name__icontains=search) | Q(serial__icontains=search),is_available = True)

    context = {
        'eqs': eqs,
        'eqActivities': eqActivities,
        'members': members
    }
    return render(request,"equipment/book.html",context)

def book(request):
    if request.method == "POST":
        serial = request.POST.get("serial")
        memId = request.POST.get("memId")
        date = request.POST.get("date")

        start_time = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        end_time = start_time + timedelta(hours=1)

        today = datetime.now().date()
        input_date = start_time.date()
        day_gap = (input_date - today).days

        if day_gap < 0:
            messages.error(request,"Past Date Selected")
            return redirect("/equipment/activity/")
        elif day_gap > 1:
            messages.error(request,"Cannot book in 2  days advanced")
            return redirect("/equipment/activity/")

        # For member
        current_day = (datetime.now()).strftime('%A')

        selectedStartTime = start_time.time()
        selectedEndTime = end_time.time()
        try:
            eq = Equipment.objects.get(serial = serial)
            try:
                member = Member.objects.get(memberId=memId)
                if member.status == False:
                    messages.error(request,"Member Account Deactivated")      
                else:
                    # Check if member package supports selected time
                    check_start_time = False
                    check_end_time = False        
                    schedules = member.package.get_schedules_filter(current_day)
                    for sc in schedules:
                        if sc.start_time <= selectedStartTime <= sc.end_time:
                            check_start_time = True

                        if sc.start_time <= selectedEndTime <= sc.end_time:
                            check_end_time = True
                    if check_start_time == False or check_end_time == False:
                        messages.error(request,"Member Package Does not support selected time")
                        return redirect("/equipment/activity/")
                    # Check if member package supports selected equipment   
                    flag = False                
                    for eqT in eq.get_eqTypes():
                        for packageEqT in member.package.get_equipmentTypes():
                            if eqT.id == packageEqT.id:
                                flag = True
                    # Equipment and Member Correct  
                    if flag:
                        eqActivityCount = EquipmentActivityTrack.objects.filter(Q(start_time__range=(start_time,end_time)) | Q(end_time__range=(start_time,end_time)),equipment = eq,is_active = True).count()
                        if eqActivityCount != 0:
                            messages.error(request,"Schedule Already Booked")
                        else:
                            EquipmentActivityTrack.objects.create(
                                start_time = start_time,
                                end_time = end_time,
                                booked_by= request.user,
                                booked_for = member,
                                equipment = eq
                            )    
                    else:
                        messages.error(request,"Member Package Doesn't Support Selected Equipment")           
            except:
                messages.error(request,"Wrong Member Id")    
        except:
            messages.error(request,"Wrong Equipment Serial")
    return redirect("/equipment/activity/")

def deactivate(request,pk):
    eq = Equipment.objects.get(id = pk)
    eq.is_available = False
    eq.save()
    return redirect("/equipment/")

def active(request,pk):
    eq = Equipment.objects.get(id = pk)
    eq.is_available = True
    eq.maintenanceDate = datetime.now()
    eq.save()
    return redirect("/equipment/")

def delete(request,pk):
    Equipment.objects.get(id = pk).delete()
    return redirect("/equipment/")
