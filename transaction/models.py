from django.db import models
from django.utils.translation import gettext_lazy as _
from member.models import Member
from user.models import User
from coach.models import Coach
from equipment.models import Equipment
from product.models import Product

DEBIT_REASONS = [
    ('admission', 'Admission'),
    ('package_fee', 'Package Fee'),
    ('private_session', 'Private Session'),
]

CREDIT_REASONS = [
    ('salary_coach', 'Coach Salary'),
    ('salary_employee', 'Employee Salary'),
    ('buy_equipment', 'Buy Equipment'),
]

MONTH_CHOICES = [
    ('January', 'January'), 
    ('February', 'February'), 
    ('March', 'March'), 
    ('April', 'April'), 
    ('May', 'May'), 
    ('June', 'June'), 
    ('July', 'July'), 
    ('August', 'August'), 
    ('September', 'September'), 
    ('October', 'October'), 
    ('November', 'November'), 
    ('December', 'December')
]

# Create your models here.
# Incoming
class Debit(models.Model):
    trxId = models.CharField(_("Transaction Id"),max_length=20,null=True,blank=True)

    reason = models.CharField(_("Reason"),max_length=50, null=True,blank=True,choices=DEBIT_REASONS)

    amount = models.FloatField(_("Amount"),null=True,blank=True)
    date = models.DateTimeField(_("Date"), null=True,blank=True)
    payed_by = models.ForeignKey(Member, on_delete=models.CASCADE,null=True,blank=True)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) :
        return f'{self.trxId} - {self.amount}'
    
# Outgoing
class Credit(models.Model):
    trxId = models.CharField(_("Transaction Id"),max_length=20,null=True,blank=True)

    reason = models.CharField(_("Reason"),max_length=50, null=True,blank=True,choices=CREDIT_REASONS)

    amount = models.FloatField(_("Amount"),null=True,blank=True)
    date = models.DateTimeField(_("Date"), null=True,blank=True)
    is_employee = models.BooleanField(_("Is Employee"),default=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    is_coach= models.BooleanField(_("Is Coach"),default=False)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE,null=True,blank=True)
    is_equipment= models.BooleanField(_("Is Equipment"),default=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self) :
        return f'{self.trxId} - {self.amount}'


class Bill(models.Model):
    month =  models.CharField(_("Month"),max_length=20,null=True,blank=True,choices=MONTH_CHOICES)
    year = models.IntegerField(_("Year"),null=True,blank=True)
    
    reason = models.CharField(_("Reason"),max_length=50, null=True,blank=True,choices=DEBIT_REASONS)
    
    total_amount = models.FloatField(_("Total Amount"),default = 0)
    payed_amount = models.FloatField(_("Payed Amount"),default = 0)
    due_amount = models.FloatField(_("Due Amount"),default = 0)
    advanced_amount = models.FloatField(_("Advanced Amount"),default = 0)
    member = models.ForeignKey(Member, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) :
        return f'{self.month} - {self.member.name}'
