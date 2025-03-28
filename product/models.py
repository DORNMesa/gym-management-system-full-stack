from django.db import models
from django.utils.translation import gettext_lazy as _

class ProductCategory(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    stock = models.IntegerField(_("Stock"), default=0)
    description = models.TextField(_("Description"), null=True, blank=True)
    is_available = models.BooleanField(_("Available"), default=True)
    image = models.ImageField(_("Image"), upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price}"

class ProductSale(models.Model):
    credit = models.ForeignKey('transaction.Credit', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
