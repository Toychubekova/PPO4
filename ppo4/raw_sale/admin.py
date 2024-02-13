from django.contrib import admin

# Register your models here.
from django.contrib import admin

from raw_sale.models import RawSale, Budget

# Register your models here.
admin.site.register(Budget)
admin.site.register(RawSale)