from django.contrib import admin

# Register your models here.

from .models import Company
from .models import Department
from .models import DepartmentGroup

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(DepartmentGroup)