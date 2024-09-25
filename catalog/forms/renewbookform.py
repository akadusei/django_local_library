import datetime

from django.core.exceptions import ValidationError
from django.forms import DateField, Form
from django.utils.translation import gettext_lazy as _

class RenewBookForm(Form):
    renewal_date = DateField(
        help_text='Enter a date between now and 4 weeks (default 3).',
        label='Renewal date',
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(
                _('Invalid date - renewal in the past'),
                code='invalid_date'
            )

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'),
                code='invalid_date'
            )

        return data
