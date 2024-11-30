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

from crispy_forms.helper import FormHelper

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class editPowCampForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wide-input'
        })
    )
    nearest_city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wide-input'
        }),
        required=False
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'wide-input'
        }),
        required=False
    )
    wartime_country = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wide-input'
        }),
        required=False
    )
    latitude = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wide-input'
        }),
        required=False
    )
    longitude = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wide-input'
        }),
        required=False
    )

    class Meta:
        model = PowCamp
        fields = '__all__'


class editCemeteryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wide-input',
            'style': 'width: 500px;'
        })
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all().order_by('name'),
        empty_label="Select a country"
    )

    class Meta:
        model = Cemetery
        fields = ['name', 'country', 'latitude', 'longitude']


class editCountryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
    class Meta:
        model = Country
        fields = "__all__"

class editAcknowledgementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
    class Meta:
        model = Acknowledgement
        created_at = forms.DateTimeField(disabled=True, required=False)
        exclude = ['created_at']  # This will hide created_at from the form
        fields = '__all__'


class editCompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
    class Meta:
        model = Company 
        fields = "__all__"

class editDecorationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
    class Meta:
        model = Decoration
        fields = "__all__"


class editRankForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wide-input',
        })
    )

    class Meta:
        model = Rank
        fields = '__all__'


class editSoldierDeathForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
    class Meta:
        model = SoldierDeath
        fields = ["date", "cemetery", "image"]  


class editSoldierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
    class Meta:
        model = Soldier
        fields = "__all__"


class ProvostOfficerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
        super().__init__(*args, **kwargs)
        self.fields['rank'].queryset = Rank.objects.filter(rank_class="OF").order_by('name')
    provost_officer = forms.BooleanField(
        initial=True,
        disabled=True,
        required=True,
        help_text="All officers created through this form are automatically marked as Provost Officers"
    )
    class Meta:
        model = Soldier
        fields = ['surname', 'initials', 'army_number', 'rank', 'provost_officer', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    def save(self, commit=True):
        soldier = super().save(commit=False)
        soldier.provost_officer = True  # Set provost_officer to True
        print(soldier)
        if commit:
            soldier.save()
        return soldier


class ProvostAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
        
    class Meta:
        model = ProvostAppointment
        fields = ['rank', 'date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class AcknowledgementForm(forms.ModelForm):
    class Meta:
        model = Acknowledgement
        fields = ['surname', 'name', 'notes']
