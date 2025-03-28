from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from transaction.models import Credit, Debit
from product.models import Product

class ReportGenerator:
    @staticmethod
    def generate_financial_report(start_date, end_date):
        report = {
            'total_revenue': Debit.objects.filter(
                date__range=[start_date, end_date],
                reason__in=['admission', 'package_fee', 'private_session']
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            
            'total_expenses': Credit.objects.filter(
                date__range=[start_date, end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        
        # Add product reports
        low_stock_threshold = 10
        
        report['low_stock_products'] = Product.objects.filter(
            stock__lte=low_stock_threshold
        ).select_related('category')
        
        report['inventory'] = Product.objects.annotate(
            total_value=ExpressionWrapper(
                F('stock') * F('price'),
                output_field=DecimalField()
            )
        ).select_related('category')
        
        report['sales'] = Credit.objects.filter(
            date__range=[start_date, end_date],
            reason='product_sale'
        ).select_related('equipment', 'coach', 'employee')
        
        report['total_inventory_value'] = sum(
            product.total_value for product in report['inventory']
        )
        
        report['total_sales_value'] = sum(
            sale.amount for sale in report['sales']
        )
        
        return report


