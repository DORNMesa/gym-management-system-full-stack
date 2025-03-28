from django.db.models import Sum
from transaction.models import Credit, Debit

class ReportGenerator:
    @staticmethod
    def generate_financial_report(start_date, end_date):
        return {
            'total_income': Debit.objects.filter(
                date__range=[start_date, end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            
            'total_revenue': Debit.objects.filter(
                date__range=[start_date, end_date],
                reason__in=['admission', 'package_fee', 'private_session']
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
        }