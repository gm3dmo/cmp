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
from crispy_forms.layout import Layout, Field, Submit, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup, TabHolder, Tab


class SoldierImprisonmentForm(forms.ModelForm):
    date_from = forms.DateField(
        initial='1940-01-01',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 20%;'
            }
        ),
        required=False
    )
    date_to = forms.DateField(
        initial='1940-01-01',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 20%;'
            }
        ),
        required=False
    )

    class Meta:
        model = SoldierImprisonment
        fields = ['pow_camp', 'pow_number', 'date_from', 'date_to', 'notes']
        widgets = {
            'date_to': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pow_camp'].required = False
        self.fields['pow_number'].required = False
        self.fields['date_to'].required = False
        self.fields['notes'].required = False

class SoldierImprisonmentFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        
        # Default to collapsed
        has_data = False
        title = 'Prisoner of War Details (None Recorded)'
        
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    title,
                    'pow_camp',
                    'pow_number',
                    'date_from',
                    'date_to',
                    'notes',
                    active=has_data,  # Collapsed by default
                    css_class='bg-info bg-opacity-25 border rounded p-3'
                ),
                css_id="imprisonment-details-accordion"
            )
        )

    def update_title(self):
        """Update the title based on formset data"""
        if hasattr(self, 'formset') and self.formset.initial_forms:
            has_data = any(form.initial for form in self.formset.initial_forms)
            title = 'Prisoner of War Details' if has_data else 'Prisoner of War Details (None Recorded)'
            self.layout[0][0].name = title
            self.layout[0][0].active = has_data

# Create the formset
SoldierImprisonmentInlineFormSet = inlineformset_factory(
    Soldier,
    SoldierImprisonment,
    form=SoldierImprisonmentForm,
    extra=1,
    can_delete=True
)

class SoldierImprisonmentFormSetWithHelper(SoldierImprisonmentInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = SoldierImprisonmentFormSetHelper()
        self.helper.formset = self
        self.helper.update_title()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username",)


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

class AcknowledgementForm(forms.ModelForm):
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
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Don't create the helper here - it will be set by the view
        self.helper = None  # We'll set this in the view
        # Order cemeteries alphabetically by name
        self.fields['cemetery'].queryset = Cemetery.objects.order_by('name')


class editSoldierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'  
        self.fields['provost_officer'].disabled = True

        # Initialize both formsets with helpers
        self.imprisonment_formset = SoldierImprisonmentFormSetWithHelper(
            instance=self.instance,
            prefix='imprisonment'
        )
        
        self.decoration_formset = SoldierDecorationFormSetWithHelper(
            instance=self.instance,
            prefix='decoration'
        )

        # Determine header classes and active states
        header_class = 'bg-light' if self.instance and self.instance.pk else 'bg-light-blue'
        
        # Check for existing imprisonments
        has_imprisonment = False
        if self.instance and self.instance.pk:
            has_imprisonment = SoldierImprisonment.objects.filter(soldier=self.instance).exists()
        
        # Check for existing decorations
        has_decorations = False
        if self.instance and self.instance.pk:
            has_decorations = SoldierDecoration.objects.filter(soldier=self.instance).exists()
        
        imprisonment_title = 'Prisoner of War Details' if has_imprisonment else 'Prisoner of War Details (None Recorded)'
        decoration_title = 'Decoration Details' if has_decorations else 'Decoration Details (None Recorded)'
        
        self.helper.layout = Layout(
            Field('surname'),
            Field('initials'),
            Field('army_number'),
            Field('rank'),
            Field('provost_officer'),
            Field('notes'),
            Accordion(
                AccordionGroup(
                    imprisonment_title,
                    'imprisonment_formset',
                    active=has_imprisonment,
                    button_class=header_class
                ),
                AccordionGroup(
                    decoration_title,
                    'decoration_formset',
                    active=has_decorations,
                    button_class=header_class
                ),
                css_id="soldier-details-accordion"
            )
        )

    class Meta:
        model = Soldier
        fields = ['surname', 'initials', 'army_number', 'rank', 'notes', 'provost_officer']
        exclude = ['created_at']


class ProvostOfficerSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by surname or army number...'
        })
    )

class ProvostOfficerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'
        
        # Filter rank choices to only show officer ranks
        self.fields['rank'].queryset = Rank.objects.filter(rank_class="OF").order_by('name')
        
        # Set provost_officer field
        self.fields['provost_officer'] = forms.BooleanField(
            initial=True,
            disabled=True,
            required=False,
            help_text="All officers created through this form are automatically marked as Provost Officers"
        )
        
        # Determine header class and active state
        header_class = 'bg-light' if self.instance and self.instance.pk else 'bg-light-blue'
        is_active = bool(self.instance and self.instance.pk)
        
        self.helper.layout = Layout(
            Field('surname'),
            Field('initials'),
            Field('army_number'),
            Field('rank'),
            Field('provost_officer'),
            Accordion(
                AccordionGroup(
                    'Appointment Details',
                    'appointment_formset',
                    active=is_active,
                    button_class=header_class
                ),
                css_id="appointment-details-accordion"
            ),
            Field('notes')
        )

    class Meta:
        model = Soldier
        fields = ['surname', 'initials', 'army_number', 'rank', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        soldier = super().save(commit=False)
        soldier.provost_officer = True
        if commit:
            soldier.save()
        return soldier

class ProvostAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-label'
        
        # Filter rank choices to only show officer ranks
        self.fields['rank'].queryset = Rank.objects.filter(rank_class="OF").order_by('name')
        
        self.helper.layout = Layout(
            Field('rank'),
            Field('date'),
            Field('notes')
        )

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 20%;'
            }
        ),
        required=False
    )

    class Meta:
        model = ProvostAppointment
        fields = ['rank', 'date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

# Create the formset
ProvostAppointmentInlineFormSet = inlineformset_factory(
    Soldier,
    ProvostAppointment,
    form=ProvostAppointmentForm,
    extra=1,
    can_delete=True
)

class ProvostAppointmentFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        
        # Default to collapsed
        has_data = False
        title = 'Appointment Details (None Recorded)'
        
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    title,
                    'rank',
                    'date',
                    'notes',
                    active=has_data,
                    css_class='bg-info bg-opacity-25 border rounded p-3'
                ),
                css_id="appointment-details-accordion"
            )
        )

    def update_title(self):
        if hasattr(self, 'formset') and self.formset.initial_forms:
            has_data = any(form.initial for form in self.formset.initial_forms)
            title = 'Appointment Details' if has_data else 'Appointment Details (None Recorded)'
            self.layout[0][0].name = title
            self.layout[0][0].active = has_data

class ProvostAppointmentFormSetWithHelper(ProvostAppointmentInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = ProvostAppointmentFormSetHelper()
        self.helper.formset = self
        self.helper.update_title()


class SoldierDecorationForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
    )

    class Meta:
        model = SoldierDecoration
        fields = ['decoration', 'gazette_issue', 'gazette_page', 'gazette_date', 'country', 'citation', 'notes']
        widgets = {
            'gazette_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'style': 'width: 20%;'
                }
            )
        }

class SoldierDecorationFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        
        # Default to collapsed
        has_data = False
        title = 'Decoration Details (None Recorded)'
        
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    title,
                    'decoration',
                    'gazette_issue',
                    'gazette_page',
                    'gazette_date',
                    'country',
                    'citation',
                    'notes',
                    active=has_data,
                    css_class='bg-info bg-opacity-25 border rounded p-3'
                ),
                css_id="decoration-details-accordion"
            )
        )

    def update_title(self):
        if hasattr(self, 'formset') and self.formset.initial_forms:
            has_data = any(form.initial for form in self.formset.initial_forms)
            title = 'Decoration Details' if has_data else 'Decoration Details (None Recorded)'
            self.layout[0][0].name = title
            self.layout[0][0].active = has_data

# Create the formset
SoldierDecorationInlineFormSet = inlineformset_factory(
    Soldier,
    SoldierDecoration,
    form=SoldierDecorationForm,
    extra=1,
    can_delete=True
)

# Add the helper to the formset
class SoldierDecorationFormSetWithHelper(SoldierDecorationInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = SoldierDecorationFormSetHelper()
        self.helper.formset = self
        self.helper.update_title()


class SoldierDeathFormHelper(FormHelper):
    def __init__(self, *args, has_image=False, image_url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        
        # Default to collapsed
        has_data = False
        title = 'Death Details (None Recorded)'
        
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    title,
                    'date',
                    'company',
                    'cemetery',
                    'cwgc_id',
                    'image',
                    HTML("""
                        {% if has_image %}
                            <div class="row">
                                <div class="col-lg-2 form-label">Current Image</div>
                                <div class="col-lg-8">
                                    <img src="{{ image_url }}" alt="Grave image" style="max-width: 200px; height: auto;" class="img-thumbnail mt-2">
                                </div>
                            </div>
                        {% endif %}
                    """),
                    active=has_data,
                    css_class='bg-info bg-opacity-25 border rounded p-3'
                ),
                css_id="death-details-accordion"
            )
        )
        # Store the image info
        self.has_image = has_image
        self.image_url = image_url

    def update_title(self):
        """Update the title based on form data"""
        if hasattr(self, 'form') and self.form.initial:
            has_data = any(self.form.initial.values())
            title = 'Death Details' if has_data else 'Death Details (None Recorded)'
            self.layout[0][0].name = title
            self.layout[0][0].active = has_data


