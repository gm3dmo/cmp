from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from .models import CustomUser

from .models import Country
from .models import Rank
from .models import Cemetery
from .models import PowCamp
from .models import Soldier
from .models import SoldierDeath
from .models import Company
from .models import Decoration
from .models import Acknowledgement
from .models import ProvostAppointment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class editPowCampForm(forms.ModelForm):
    class Meta:
        model = PowCamp
        fields = "__all__"


class editCemeteryForm(forms.ModelForm):
    class Meta:
        model = Cemetery 
        fields = "__all__"


class editCountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = "__all__"

class editAcknowledgementForm(forms.ModelForm):

    class Meta:
        model = Acknowledgement
        created_at = forms.DateTimeField(disabled=True, required=False)
        exclude = ['created_at']  # This will hide created_at from the form
        fields = '__all__'


class editCompanyForm(forms.ModelForm):
    class Meta:
        model = Company 
        fields = "__all__"

class editDecorationForm(forms.ModelForm):
    class Meta:
        model = Decoration
        fields = "__all__"


class editRankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = "__all__"


class editSoldierDeathForm(forms.ModelForm):
    class Meta:
        model = SoldierDeath
        fields = ["date", "cemetery", "image"]  


class editSoldierForm(forms.ModelForm):
    class Meta:
        model = Soldier
        fields = "__all__"


class ProvostOfficerForm(forms.ModelForm):
    class Meta:
        model = Soldier
        fields = ['id', 'surname', 'initials', 'army_number', 'rank', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rank'].queryset = Rank.objects.filter(rank_class="OF").order_by('name')

    def save(self, commit=True):
        soldier = super().save(commit=False)
        soldier.provost_officer = True  # Set provost_officer to True
        print(soldier)
        if commit:
            soldier.save()
        return soldier

class ProvostAppointmentForm(forms.ModelForm):
    class Meta:
        model = ProvostAppointment
        fields = ['soldier', 'rank', 'date', 'notes']


