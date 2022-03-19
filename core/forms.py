from django import forms
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from import_export.forms import ConfirmImportForm, ImportForm
from django.utils.translation import gettext as _

import calendar
import datetime


def get_months():
    today = timezone.now().date()
    months = []
    month_count = 0
    while month_count < 24:
        month = today - relativedelta(months=month_count)
        months.append((month, month.strftime("%B, %Y")))
        month_count += 1
    return months


class ConfirmImportForm(ConfirmImportForm):
    month = forms.DateField(required=True, widget=forms.HiddenInput())


class ImportForm(ImportForm):
    month = forms.DateField(input_formats=["%Y-%m-%d"], widget=forms.Select(choices=get_months(), ))

    def clean_month(self):
        month = self.cleaned_data['month']
        first_day = calendar.monthrange(month.year, month.month)[0]
        return datetime.date(month.year, month.month, first_day)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['input_format'].choices.pop(0)


class MonthForm(forms.Form):
    month = forms.DateField(input_formats=["%Y-%m-%d"])

    def clean_month(self):
        month = self.cleaned_data['month']
        first_day = calendar.monthrange(month.year, month.month)[0]
        return datetime.date(month.year, month.month, first_day)