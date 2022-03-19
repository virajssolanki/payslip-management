from django.contrib import admin
from django.utils import timezone
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportMixin, ImportExportMixin
from import_export.widgets import ForeignKeyWidget
from import_export.formats import base_formats
from django.contrib.auth.models import User, Group

import datetime

from core.forms import ConfirmImportForm, ImportForm, MonthForm
from core.models import *

admin.site.site_header = "HR Samcom"
admin.site.site_title = "Samcom"
admin.site.index_title = "Salary Navigator"

# admin.site.unregister(User)
# admin.site.unregister(Group)


class EmailForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value, row, *args, **kwargs):
        instance = self.model.objects.get_or_create(email=value, )[0]
        if instance.name != row['Name']:
            instance.name = row['Name']
            instance.save()
        return instance


class SalaryResource(resources.ModelResource):
    paid_leaves = Field(attribute='paid_leaves', column_name='PL')
    leaves = Field(attribute='leaves', column_name='Leaves')
    working_days = Field(attribute='working_days', column_name='Working Days')
    actual_days = Field(attribute='actual_days', column_name='Actual Days')
    employ_email = Field(column_name='Email', attribute='employ',
                        widget=EmailForeignKeyWidget(User, 'email'))

    class Meta:
        model = Salary
        list_display = ['month', 'id', 'paid_leaves', 'leaves', 'total_days', 'working_days', 'actual_days', 'employ']
        import_id_fields = ['employ_email', 'month']
        
    def __init__(self, request=None):
        super()
        self.request = request

    def before_import_row(self, row, **kwargs):
        form = MonthForm(self.request.POST or None)
        if form.is_valid():
            month = form.cleaned_data['month']
            self.request.session['import_context_month'] = self.request.POST.get('month')
            row['month'] = month
        pass


class SalaryAdmin(ImportExportMixin, admin.ModelAdmin):
 
    @admin.display(description='month')
    def admin_month(self, obj):
        return obj.month.strftime('%B, %Y')

    #list_display = [field.name for field in Salary._meta.fields if field.name != "id"]
    list_display = ['employ', 'admin_month', 'id', 'paid_leaves', 'leaves', 'total_days', 'working_days', 'actual_days',]
    readonly_fields = ['month', 'id', 'paid_leaves', 'leaves', 'total_days', 'working_days', 'actual_days', 'employ']
    list_filter = ['employ']
    resource_class = SalaryResource
    date_hierarchy = 'month'
    date_hierarchy_drilldown = False
    actions = ["email_payslip"]

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
        
    def email_payslip(self, request, queryset):
        print(queryset)
        
    def get_import_form(self):
        return ImportForm

    def get_confirm_import_form(self):
        return ConfirmImportForm

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        formats = [base_formats.XLSX, base_formats.CSV, base_formats.XLS,]
        return [f for f in formats if f().can_import()]

    def get_form_kwargs(self, form, *args, **kwargs):
        if isinstance(form, ImportForm):
            if form.is_valid():
                month = form.cleaned_data['month']
                kwargs.update({'month': month})
        return kwargs

    def get_resource_kwargs(self, request, *args, **kwargs):
        """
        passing request to get form in before_import_row
        """
        resource_kwargs = super().get_resource_kwargs(request, *args, **kwargs)
        resource_kwargs['request'] = request
        return resource_kwargs

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        """
        date and year filter for admin dashboard
        """
        today = timezone.now().date()
        if year_lookup is None and month_lookup is None:
            return (
                datetime.date(y, 1, 1)
                for y in range(today.year - 2, today.year + 1)
            )
        elif year_lookup is not None and month_lookup is None:
            this_month = today.replace(day=1)
            return (
                month for month in (
                    datetime.date(int(year_lookup), month, 1)
                    for month in range(1, 13)
                ) if month <= this_month
            )
        elif year_lookup is not None and month_lookup is not None:
            return []


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_staff', 'is_active']
    list_filter = ['email']


admin.site.register(Salary, SalaryAdmin)
admin.site.register(User, UserAdmin)
