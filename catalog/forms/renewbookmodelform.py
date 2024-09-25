import datetime

from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm
from django.utils.translation import gettext_lazy as _

from ..models import BookInstance

class RenewBookModelForm(ModelForm):
    virtual_field = CharField(max_length=200)

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

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

    def clean_virtual_field(self):
        # Custom validation for the virtual field
        data = self.cleaned_data['virtual_field']
        # Add your validation logic here
        return data

    class Meta:
        model = BookInstance
        fields = ('due_back', 'virtual_field')
        labels = {'due_back': _('New renewal date')}

        help_texts = {
            'due_back': _('Enter a date between now and 4 weeks (default 3).')
        }
