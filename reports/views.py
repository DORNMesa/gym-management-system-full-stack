from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from transaction.models import Credit, Debit
from member.models import Member
from equipment.models import EquipmentActivityTrack
from coach.models import CoachActivityTrack
from .report_generator import ReportGenerator
from django.contrib import messages

@login_required
def reports_view(request):
    try:
        # Set default date range to last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        if request.method == "POST":
            try:
                start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
                end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
                
                if start_date > end_date:
                    messages.error(request, "Start date cannot be after end date")
                    return redirect('reports:reports')
                    
            except ValueError:
                messages.error(request, "Invalid date format")
                return redirect('reports:reports')

        # Generate report data
        report_data = ReportGenerator.generate_financial_report(start_date, end_date)
        
        # Add additional metrics for the main report view
        report_data.update({
            'total_expenses': Credit.objects.filter(
                date__range=[start_date, end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            
            'coach_sessions': CoachActivityTrack.objects.filter(
                start_time__range=[start_date, end_date]
            ).count(),
            
            'active_members': Member.objects.filter(
                status=True
            ).count(),
            
            'new_members': Member.objects.filter(
                join_date__range=[start_date, end_date]
            ).count(),
            
            'equipment_utilization': EquipmentActivityTrack.objects.filter(
                start_time__range=[start_date, end_date]
            ).values('equipment__name').annotate(
                usage_count=Count('id')
            ).order_by('-usage_count')
        })
        
        context = {
            'report': report_data,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }
        
        return render(request, 'reports/reports.html', context)
        
    except Exception as e:
        messages.error(request, f"Error generating report: {str(e)}")
        return redirect('reports:reports')

@login_required
def print_report(request):
    # Default to last 30 days if no date range specified
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d')

    report_data = ReportGenerator.generate_financial_report(start_date, end_date)
    
    # Additional metrics
    report_data.update({
        'total_expenses': Credit.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(Sum('amount'))['amount__sum'] or 0,
        
        'coach_sessions': CoachActivityTrack.objects.filter(
            start_time__range=[start_date, end_date]
        ).count(),
        
        'active_members': Member.objects.filter(
            status=True
        ).count(),
        
        'new_members': Member.objects.filter(
            join_date__range=[start_date, end_date]
        ).count(),
        
        'equipment_utilization': EquipmentActivityTrack.objects.filter(
            start_time__range=[start_date, end_date]
        ).values('equipment__name').annotate(
            usage_count=Count('id')
        ).order_by('-usage_count')
    })

    context = {
        'report': report_data,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    
    return render(request, 'reports/print_report.html', context)







