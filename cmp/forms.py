from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from .models import CustomUser

from .models import Country
from .models import Rank
from .models import Cemetery
from .models import PowCamp
from .models import Soldier
from .models import SoldierDeath
from .models import SoldierImprisonment
from .models import SoldierDecoration
from .models import Company
from .models import Decoration
from .models import Acknowledgement
from .models import ProvostAppointment
from django.forms import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup

# First, create a helper class for the formset
class SoldierImprisonmentFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        
        # Check if there's any data in the formset
        has_data = False
        if hasattr(self, 'formset'):
            has_data = any(not form.empty_permitted or form.initial for form in self.formset)
        
        # Set title based on whether there's data
        title = 'Prisoner of War Details' if has_data else 'Prisoner of War Details (None Recorded)'
        
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    title,
                    'pow_camp',
                    'pow_number',
                    'date_from',
                    'date_to',
                    'notes',
                    active=has_data,  # Only active if there's data
                    css_class='bg-light'
                ),
                css_id="imprisonment-details-accordion"
            )
        )

# Then create the formset with the helper
SoldierImprisonmentInlineFormSet = inlineformset_factory(
    Soldier,
    SoldierImprisonment,
    fields=['pow_camp', 'pow_number', 'date_from', 'date_to', 'notes'],
    extra=1,
    can_delete=True
)

# Add the helper to the formset
SoldierImprisonmentInlineFormSet.helper = SoldierImprisonmentFormSetHelper()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class editPowCampForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        # Determine header class and active state based on whether form has data
        header_class = 'bg-light' if self.instance and self.instance.pk else 'bg-light-blue'
        is_active = bool(self.instance and self.instance.pk)
        
        self.helper.layout = Layout(
            Field('name'),
            Accordion(
                AccordionGroup(
                    'POW Details',
                    Field('nearest_city'),
                    Field('notes'),
                    Field('wartime_country'),
                    Field('latitude'),
                    Field('longitude'),
                    active=is_active,
                    button_class=header_class
                ),
                css_id="powcamp-details-accordion"
            )
        )

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
    class Meta:
        model = SoldierDeath
        fields = ['date', 'company', 'cemetery', 'cwgc_id', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        # Determine header class and active state based on whether form has data
        header_class = 'bg-light' if self.instance and self.instance.pk else 'bg-light-blue'
        is_active = bool(self.instance and self.instance.pk)
        
        # Set title based on whether there's data
        title = 'Death Details' if self.instance and self.instance.pk else 'Death Details (None Recorded)'
        
        self.helper.layout = Layout(
            Accordion(
                AccordionGroup(
                    title,
                    'date',
                    'company',
                    'cemetery',
                    'cwgc_id',
                    'image',
                    active=is_active,
                    button_class=header_class
                ),
                css_id="death-details-accordion"
            )
        )


class editSoldierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
        self.fields['provost_officer'].disabled = True


        # Determine header class and active state based on whether form has data
        header_class = 'bg-light' if self.instance and self.instance.pk else 'bg-light-blue'
        is_active = bool(self.instance and self.instance.pk)
        
        # Check if there are any imprisonment records
        has_imprisonment = False
        if self.instance and self.instance.pk:
            has_imprisonment = SoldierImprisonment.objects.filter(soldier=self.instance).exists()
        
        # Set title based on whether there's data
        title = 'Prisoner of War Details' if has_imprisonment else 'Prisoner of War Details (None Recorded)'
        
        self.helper.layout = Layout(
            Field('surname'),
            Field('initials'),
            Field('army_number'),
            Field('rank'),
            Field('provost_officer'),
            Field('notes'),
            Accordion(
                AccordionGroup(
                    title,
                    'imprisonment_formset',
                    active=has_imprisonment,
                    button_class=header_class
                ),
                css_id="imprisonment-details-accordion"
            )
        )
        # Initialize the formset
        self.imprisonment_formset = SoldierImprisonmentInlineFormSet(
            instance=self.instance,
            prefix='imprisonment'
        )

    class Meta:
        model = Soldier
        exclude = ['created_at']  # Exclude the created_at field


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

class SoldierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        
        # Determine header class and active state based on whether form has data
        header_class = 'bg-light' if self.instance and self.instance.pk else 'bg-light-blue'
        is_active = bool(self.instance and self.instance.pk)
        
        self.helper.layout = Layout(
            Field('surname'),
            Field('initials'),
            Field('army_number'),
            Field('rank'),
            #Field('provost_officer'),
            Field('notes'),
            Accordion(
                AccordionGroup(
                    'Prisoner of War Details',
                    'imprisonment_formset',
                    active=is_active,
                    button_class=header_class
                ),
                css_id="imprisonment-details-accordion"
            )
        )
        # Initialize the formset
        self.imprisonment_formset = SoldierImprisonmentInlineFormSet(
            instance=self.instance,
            prefix='imprisonment'
        )

    class Meta:
        model = Soldier
        fields = ['surname', 'initials', 'army_number', 'rank', 'provost_officer', 'notes']


class SoldierDecorationFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        
        # Check if there's any data in the formset
        has_data = False
        if hasattr(self, 'formset'):
            has_data = any(not form.empty_permitted or form.initial for form in self.formset)
        
        # Set title based on whether there's data
        title = 'Decoration Details' if has_data else 'Decoration Details (None Recorded)'
        
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    title,
                    'decoration',
                    'gazette_issue',
                    'gazette_page',
                    'gazette_date',
                    'theatre',
                    'country',
                    'citation',
                    'notes',
                    active=has_data,  # Only active if there's data
                    css_class='bg-light'
                ),
                css_id="decoration-details-accordion"
            )
        )

# Create the formset with the helper
SoldierDecorationInlineFormSet = inlineformset_factory(
    Soldier,
    SoldierDecoration,
    fields=['decoration', 'gazette_issue', 'gazette_page', 'gazette_date', 'theatre', 'country', 'citation', 'notes'],
    extra=1,
    can_delete=True
)

# Add the helper to the formset
SoldierDecorationInlineFormSet.helper = SoldierDecorationFormSetHelper()


