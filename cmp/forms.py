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
        fields = "__all__"


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


class editSoldierForm(forms.ModelForm):
    class Meta:
        model = Soldier
        fields = "__all__"


class editSoldierDeathForm(forms.ModelForm):
    class Meta:
        model = SoldierDeath
        fields = ["date", "cemetery", "image"]  

