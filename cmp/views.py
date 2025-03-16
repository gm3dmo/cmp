from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, HttpResponse

from django.db.models import Q, Count, F
from django.db.models.functions import Cast, ExtractYear
from django.db.models import FloatField

from django.contrib.auth.decorators import login_required

from .models import Acknowledgement
from cmp.forms import AcknowledgementForm

from .models import Country
from cmp.forms import editCountryForm

from .models import Company
from cmp.forms import editCompanyForm

from .models import Decoration
from cmp.forms import editDecorationForm

from .models import Rank
from cmp.forms import editRankForm

from .models import Cemetery 
from cmp.forms import editCemeteryForm

from .models import PowCamp
from cmp.forms import editPowCampForm

from .models import Soldier
from cmp.forms import editSoldierForm

from .models import SoldierDeath
 
from .models import SoldierDecoration

from django.shortcuts import render, redirect

from .models import SoldierImprisonment

from .forms import (
    editSoldierForm, editSoldierDeathForm,
    SoldierImprisonmentFormSetWithHelper,
    SoldierDecorationInlineFormSet,
    SoldierDecorationFormSetWithHelper,
    SoldierDeathFormHelper
)
from .forms import SoldierDecorationInlineFormSet
from .forms import ProvostOfficerForm, ProvostAppointmentForm
from .forms import SoldierImprisonmentFormSetHelper, SoldierDecorationFormSetHelper
from .forms import ProvostAppointmentFormSetWithHelper, SoldierDecorationFormSetWithHelper

from .models import ProvostAppointment

import folium
from django.views.generic import TemplateView
import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Acknowledgement
from .forms import AcknowledgementForm

from django.contrib import messages

from .models import ProvostAppointment

from django.utils.html import format_html
from django.urls import reverse

import os

logger = logging.getLogger(__name__)

def mgmt_index(request):
    return render(request, 'cmp/mgmt-index.html')


def powcamps(request):
    powcamps = PowCamp.objects.all()
    return render(request, 'cmp/pow-camps.html', {'powcamps': powcamps})


def cemeteries(request):
    cemeteries = Cemetery.objects.all()
    return render(request, 'cmp/cemeteries.html', {'cemeteries': cemeteries})


def countries(request):
    countries = Country.objects.all()
    return render(request, 'cmp/countries.html', {'countries': countries})


def soldiers(request):
    soldiers = Soldier.objects.all()
    return render(request, 'cmp/soldiers.html', {'soldiers': soldiers})


def ranks(request):
    ranks = Rank.objects.all()
    return render(request, 'cmp/ranks.html', {'ranks': ranks})

def acknowledgements(request):
    acknowledgements = Acknowledgement.objects.all()
    return render(request, 'cmp/acknowledgements.html', {'acknowledgements': acknowledgements})


#def index(request):
#    return render(request, "cmp/index.html")


def army_number_search(request):
    post = request.POST
    if post:
        try:
            army_number = int(post.get("q"))
        except ValueError:
            return HttpResponse("Please enter a valid Army Number")
        return original_unit(request, army_number)
    return render(request, "cmp/army-number-search.html")


def trigger_error(request):
    """error for Sentry"""
    division_by_zero = 1 / 0


def belongsTo(value: int, rangeStart: int, rangeEnd: int):
    if type(value) != int:
        return False
    elif value >= rangeStart and value <= rangeEnd:
        return True
    else:
        return False


def original_unit(request, army_number):
    army_number_index = {
        "Royal Army Service Corps (Block 1)": [1, 294000],
        "Royal Army Service Corps (Block 2)": [10660001, 11000000],
        "1st Life Guards": [294001, 299000],
        "2nd Life Guards": [299001, 304000],
        "Royal Horse Guards": [304001, 309000],
        # Cavalry of the Line 309001 - 721000 (Inclusive 558471 to 558761 allocated to the Royal Armoured Corps extraordinary to the block of numbers later allocated)
        "Lancers": [309001, 386000],
        "Dragoons": [386001, 528000],
        "Hussars": [528001, 721000],
        "Royal Artillery (Field, Coastal & Anti-Aircraft) 1": [721001, 1842000],
        "Royal Artillery (Field, Coastal & Anti-Aircraft) 2": [11000001, 11500000],
        "Royal Engineers": [1842001, 2303000],
        "Royal Corps of Signals": [2303001, 2604000],
        "Grenadier Guards": [2604001, 2646000],
        "Coldstream Guards": [2646001, 2688000],
        "Scots Guards": [2688001, 2714000],
        "Irish Guards": [2714001, 2730000],
        "Welsh Guards": [2730001, 2744000],
        "Black Watch (The Royal Highland Regiment)": [2744001, 2809000],
        "Seaforth Highlanders": [2809001, 2865000],
        "Gordon Highlanders": [2865001, 2921000],
        "Cameron Highlanders": [2921001, 2966000],
        "Argyll & Sutherland Highlanders": [2966001, 3044000],
        "Royal Scots": [3044001, 3122000],
        "Royal Scots Fusiliers": [3122001, 3178000],
        "The King's Own Scottish Borderers": [3178001, 3233000],
        "Cameronians (Scottish Rifles)": [3233001, 3299000],
        "Highland Light Infantry": [3299001, 3377000],
        "East Lancashire Regiment": [3377001, 3433000],
        "Lancashire Fusiliers": [3433001, 3511000],
        "Manchester Regiment": [3511001, 3589000],
        "Border Regiment": [3589001, 3644000],
        "The Prince of Wales Volunteers": [3644001, 3701000],
        "The King's Own Royal Regiment": [3701001, 3757000],
        "The King's Regiment": [3757001, 3846000],
        "The Loyal Regiment": [3846001, 3902000],
        "South Wales Borderers": [3902001, 3947000],
        "Welch Regiment": [3947001, 4025000],
        "The King's Shropshire Light Infantry": [4025001, 4070000],
        "Monmouthshire Regiment": [4070001, 4103000],
        "Herefordshire Regiment": [4103001, 4114000],
        "Cheshire Regiment": [4114001, 4178000],
        "Royal Welch Fusiliers": [4178001, 4256000],
        "Royal Northumberland Fusiliers": [4256001, 4334000],
        "East Yorkshire Regiment": [4334001, 4379000],
        "The Green Howards": [4379001, 4435000],
        "Durham Light Infantry": [4435001, 4523000],
        "West Yorkshire Regiment": [4523001, 4601000],
        "The Duke of Wellington's Regiment (The West Riding)": [4601001, 4680000],
        "The King's Own Yorkshire Light Infantry": [4680001, 4736000],
        "York & Lancaster Regiment": [4736001, 4792000],
        "Lincolnshire Regiment": [4792001, 4848000],
        "Leicestershire Regiment": [4848001, 4904000],
        "South Staffordshire Regiment": [4904001, 4960000],
        "Sherwood Foresters": [4960001, 5038000],
        "North Staffordshire Regiment": [5038001, 5094000],
        "Royal Warwickshire Regiment": [5094001, 5172000],
        "Gloucestershire Regiment": [5172001, 5239000],
        "Worcestershire Regiment": [5239001, 5328000],
        "Royal Berkshire Regiment": [5328001, 5373000],
        "Oxfordshire & Buckinghamshire Light Infantry": [5373001, 5429000],
        "The Duke of Cornwall's Light Infantry": [5429001, 5485000],
        "Hampshire Regiment": [5485001, 5562000],
        "Wiltshire Regiment": [5562001, 5608000],
        "Devonshire Regiment": [5608001, 5662000],
        "Somerset Light Infantry": [5662001, 5718000],
        "Dorsetshire Regiment": [5718001, 5763000],
        "Royal Norfolk Regiment": [5763001, 5819000],
        "Suffolk Regiment": [5819001, 5875000],
        "Northamptonshire Regiment": [5875001, 5931000],
        "Cambridgeshire Regiment": [5931001, 5942000],
        "Bedfordshire & Hertfordshire Regiment": [5942001, 5998000],
        "Essex Regiment": [5998001, 6076000],
        "The Queen's Royal Regiment": [6076001, 6132000],
        "East Surrey Regiment": [6132001, 6188000],
        "Middlesex Regiment": [6188001, 6278000],
        "The Buffs (East Kent Regiment)": [6278001, 6334000],
        "Royal West Kent Regiment": [6334001, 6390000],
        "Royal Sussex Regiment": [6390001, 6446000],
        "Royal Fusiliers": [6446001, 6515000],
        "London Regiment": [6515001, 6802500],
        "The Inns of Court Regiment": [6802501, 6814000],
        "Honourable Artillery Company (Infantry)": [6825001, 6837000],
        "The King's Royal Rifle Corps": [6837001, 6905000],
        "The Rifle Brigade": [6905001, 6972000],
        "Royal Inniskilling Fusiliers": [6972001, 7006000],
        "Royal Ulster Rifles": [7006001, 7040000],
        "Royal Irish Fusiliers": [7040001, 7075000],
        "Royal Dublin Fusiliers (Disbanded 1922)": [7075001, 7109000],
        "Royal Irish Regiment": [7109001, 7143000],
        "Connaught Rangers (Disbanded 1922)": [7143001, 7177000],
        "Leinster Regiment (Disbanded 1922)": [7177001, 7211000],
        "Royal Munster Fusiliers (Disbanded 1922)": [7211001, 7245000],
        "Royal Army Medical Corps": [7245001, 7536000],
        "(Royal) Army Dental Corps (Block 1)": [7536001, 7539000],
        "(Royal) Army Dental Corps (Block 2)": [10510001, 10530000],
        "Royal Guernsey Militia and Royal Alderney Artillery Militia (Discontinued 1929)": [
            7539001,
            7560000,
        ],
        "Royal Militia of the Island of Jersey (Discontinued 1929)": [7560001, 7574000],
        "Royal Army Ordnance Corps (Block 1)": [7574001, 7657000],
        "Royal Army Ordnance Corps (Block 2)": [10530001, 10600000],
        "(Royal) Army Pay Corps (Block 1)": [7657001, 7681000],
        "(Royal) Army Pay Corps (Block 2)": [10400001, 10500000],
        "(Locally enlisted staff Middle East)": [10500001, 10508000],
        "(Royal) Military Police": [7681001, 7717000],
        "Military Provost Staff Corps": [7717001, 7718800],
        "Small Arms School Corps": [7718801, 7720400],
        "(Royal) Army Education Corps": [7720401, 7732400],
        "Band of the Royal Military College": [7732401, 7733000],
        "Corps of Military Accountants (Disbanded 1925)": [7733001, 7757000],
        "Royal Army Veterinary Corps": [7757001, 7807000],
        "Machine Gun Corps (Disbanded 1922)": [7807001, 7868000],
        "Royal Tank Regiment": [7868001, 7891868],
        "Royal Armoured Corps (Block 1)": [7891869, 8230000],
        "Royal Armoured Corps (Block 2)": [558471, 558761],
        #'Militia 10000000 - 10350000 (Army Numbers were allocated in accordance with Regulations for the Militia [Other than the Supplementary Reserve], 1939, paras. 11-13)
        "Intelligence Corps": [10350001, 10400000],
        "Reconnaissance Corps": [10600001, 10630000],
        "Army Catering Corps": [10630001, 10655000],
        "Army Physical Training (Staff) Corps": [10655001, 10660000],
        "(Royal) Pioneer Corps": [13000001, 14000000],
        "The Lowland Regiment": [14000001, 14002500],
        "The Highland Regiment": [14002501, 14005000],
        "General Service Corps": [14200001, 15000000],
        "Indian local enlistments": [15000001, 15005000],
        "Royal Electrical & Mechanical Engineers": [16000001, 16100000],
        "Non-Combatant Corps": [97000001, 97100000],
        # Auxiliary Territorial Service W/1 - W/500,000
        # Voluntary Aid Detachments W/500001 - W/1000000
        # Post War Numbering system.
        "Until October 1950": [22000000, 22199408],
        "November 1950 until February 1951": [22199409, 22460786],
        "February 1951 until July 1951": [22460787, 22562759],
        "July 1951 until June 1955": [22562760, 23052500],
        "June 1955 until October 1955": [23052501, 23188252],
        "October 1955 until May 1956": [23188253, 23479123],
        "May 1956 until October 1960": [23479124, 23845071],
        "October 1960 until April 1964": [23845072, 23969619],
        "April 1964 until October 1964": [23969620, 24033484],
        "Until April 1965": [24033485, 24057159],
        "Until December 1966": [24057160, 24076468],
        "Until April 1969": [24076469, 24182226],
        "Until September 1971": [24182227, 24262662],
        "Until September 1972": [24262663, 24302033],
        "Until January 1973": [24302034, 24315610],
        "Until February 1973": [24315611, 24322198],
        "Until August 1974": [24322199, 24355527],
        "Until September 1975": [24355528, 24369281],
        "Until May 1978": [24369282, 24475540],
        "Until March 1979": [24475541, 24520161],
        "Until August 1980": [24520162, 24579860],
        "Until December 1985": [24587119, 24753060],
        "Until November 1988": [24753061, 24854044],
        "Until January 1992": [24854045, 25012465],
        "January 1992 to July 1993": [25012466, 25027818],
        "July 1993 to August 1995": [25027819, 25041250],
        "August 1995 to July 1997": [25041251, 25065603],
        "January 1998 to January 1999": [25073583, 25087140],
        "January 1999 to September 2000": [25087141, 25122315],
        "September 2000 to April 2001": [25122316, 25112186],
        "August 2001 to July 2003": [25136866, 25139703],
        "Jul 2003 to Sep 2003 ": [25170931, 25177141],
        "Oct 2003 to Jun 2004 ": [25177142, 25189124],
    }
    for unit in army_number_index:
        # Uncomment this breakpoint to work with ipdb:
        # breakpoint()
        # embed()
        original_unit = belongsTo(
            army_number, army_number_index[unit][0], army_number_index[unit][1]
        )
        if original_unit is True:
            return HttpResponse(unit)
    return HttpResponse("No Match Found")


def edit_cemeteries(request, id=None):
    if id:
        cemetery = get_object_or_404(Cemetery, id=id)
        if request.method == 'POST':
            form = editCemeteryForm(request.POST, instance=cemetery)
        else:
            form = editCemeteryForm(instance=cemetery)
    else:
        cemetery = None
        form = editCemeteryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        cemetery = form.save()
        messages.success(request, f'Cemetery "{cemetery.name}" successfully {"updated" if id else "added"}!')
        return redirect('search-cemeteries')

    return render(request, 'cmp/edit-cemeteries.html', {
        'form': form,
        'cemetery': cemetery
    })


def edit_powcamps(request, id=None):
    if id:
        powcamp = get_object_or_404(PowCamp, id=id)
        if request.method == 'POST':
            form = editPowCampForm(request.POST, instance=powcamp)
        else:
            form = editPowCampForm(instance=powcamp)
    else:
        powcamp = None
        form = editPowCampForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        powcamp = form.save()
        messages.success(request, f'PoW Camp "{powcamp.name}" successfully {"updated" if id else "added"}!')
        return redirect('search-powcamps')

    return render(request, 'cmp/edit-pow-camps.html', {
        'form': form,
        'powcamp': powcamp
    })


def edit_country(request, country_id):
    post = request.POST
    form = editCountryForm(post or None)
    if country_id:
        country = Country.objects.get(id=country_id)
        form = editCountryForm(post or None, instance=country)
    if post and form.is_valid():
        form.save()
        return HttpResponse("Country Added")
    return render(request, "cmp/edit-countries.html", {"form": form})


def edit_companies(request, id=None):  # Changed parameter name to match URL
    if id:
        company = get_object_or_404(Company, id=id)
        if request.method == 'POST':
            form = editCompanyForm(request.POST, instance=company)
        else:
            form = editCompanyForm(instance=company)
    else:
        company = None
        form = editCompanyForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        company = form.save()
        messages.success(request, f'Company "{company.name}" successfully {"updated" if id else "added"}!')
        return redirect('search-companies')

    return render(request, 'cmp/edit-companies.html', {
        'form': form,
        'company': company
    })


def edit_decorations(request, decoration_id=None):
    if decoration_id:
        decoration = get_object_or_404(Decoration, id=decoration_id)
        if request.method == 'POST':
            form = editDecorationForm(request.POST, instance=decoration)
        else:
            form = editDecorationForm(instance=decoration)
    else:
        decoration = None
        form = editDecorationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        decoration = form.save()
        messages.success(request, f'Decoration "{decoration.name}" successfully {"updated" if decoration_id else "added"}!')
        return redirect('search-decorations')  # Redirect to search page

    return render(request, 'cmp/edit-decorations.html', {
        'form': form,
        'decoration': decoration
    })


def edit_countries(request, country_id=None):
    post = request.POST
    form = editCountryForm(post or None)
    if country_id:
        country = Country.objects.get(id=country_id)
        form = editCountryForm(post or None, instance=country)
    if post and form.is_valid():
        form.save()
        return HttpResponse("Country Added")
    return render(request, "cmp/edit-countries.html", {"form": form})


def edit_powcamps(request, id=None):  # Make sure parameter is named 'id'
    if id:
        powcamp = get_object_or_404(PowCamp, id=id)
        if request.method == 'POST':
            form = editPowCampForm(request.POST, instance=powcamp)
        else:
            form = editPowCampForm(instance=powcamp)
    else:
        powcamp = None
        form = editPowCampForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        powcamp = form.save()
        messages.success(request, f'PoW Camp "{powcamp.name}" successfully {"updated" if id else "added"}!')
        return redirect('search-powcamps')

    return render(request, 'cmp/edit-pow-camps.html', {
        'form': form,
        'powcamp': powcamp
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def soldier_detail(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)
    return render(request, 'cmp/soldier.html', {'soldier': soldier})


def edit_soldier(request, id=None):
    if id:
        soldier = get_object_or_404(Soldier, id=id)
        try:
            soldier_death = SoldierDeath.objects.get(soldier=soldier)
            # Check for image file in the expected location
            expected_image_path = os.path.join(settings.MEDIA_ROOT, str(soldier.id), 'memorial')
            # Check for common image extensions
            for ext in ['.jpg', '.jpeg', '.png']:
                potential_file = os.path.join(expected_image_path, f"{soldier.id}{ext}")
                if os.path.exists(potential_file):
                    # Convert to relative URL for template
                    relative_path = os.path.relpath(potential_file, settings.MEDIA_ROOT)
                    image_url = f"{settings.MEDIA_URL}{relative_path}"
                    has_image = True
                    break
            else:  # No image found
                has_image = False
                image_url = None
        except SoldierDeath.DoesNotExist:
            soldier_death = None
            has_image = False
            image_url = None
    else:
        soldier = None
        soldier_death = None
        has_image = False
        image_url = None

    if request.method == 'POST':
        form = editSoldierForm(request.POST, request.FILES, instance=soldier)
        death_form = editSoldierDeathForm(request.POST, request.FILES, instance=soldier_death)
        death_form.helper = SoldierDeathFormHelper(has_image=has_image, image_url=image_url)
        death_form.helper.form = death_form
        death_form.helper.update_title()
        
        decoration_formset = SoldierDecorationFormSetWithHelper(
            request.POST,
            request.FILES,
            instance=soldier,
            prefix='decoration'
        )
        
        imprisonment_formset = SoldierImprisonmentFormSetWithHelper(
            request.POST,
            request.FILES,
            instance=soldier,
            prefix='imprisonment'
        )
        
        if form.is_valid() and death_form.is_valid() and decoration_formset.is_valid() and imprisonment_formset.is_valid():
            # First save the soldier
            soldier = form.save()
            
            # Then save death form if changed
            if death_form.has_changed():
                death_instance = death_form.save(commit=False)
                death_instance.soldier = soldier
                death_instance.save()
            
            # Now save formsets with the saved soldier instance
            decoration_formset.instance = soldier
            decoration_formset.save()
            
            # Only save imprisonment forms that have data
            for imprisonment_form in imprisonment_formset:
                if imprisonment_form.has_changed() and not imprisonment_form.empty_permitted:
                    if imprisonment_form.cleaned_data.get('pow_camp'):  # Only save if pow_camp is provided
                        imprisonment = imprisonment_form.save(commit=False)
                        imprisonment.soldier = soldier
                        imprisonment.save()
            
            success_message = format_html(
                'Soldier "<a href="/soldier/{}">{} {}</a>" saved. <a href="/mgmt/soldiers/{}/edit/">View/Edit admin record</a>',
                soldier.id,
                soldier.surname,
                soldier.initials,
                soldier.id
            )
            messages.success(request, success_message)
            return redirect('search-soldiers')
        else:
            print("Form errors:", form.errors)
            print("Death form errors:", death_form.errors)
            print("Decoration formset errors:", decoration_formset.errors)
            print("Imprisonment formset errors:", imprisonment_formset.errors)
    else:
        form = editSoldierForm(instance=soldier)
        death_form = editSoldierDeathForm(instance=soldier_death)
        death_form.helper = SoldierDeathFormHelper(has_image=has_image, image_url=image_url)
        death_form.helper.form = death_form
        death_form.helper.update_title()
        
        decoration_formset = SoldierDecorationFormSetWithHelper(
            instance=soldier,
            prefix='decoration'
        )
        
        imprisonment_formset = SoldierImprisonmentFormSetWithHelper(
            instance=soldier,
            prefix='imprisonment'
        )

    context = {
        'form': form,
        'death_form': death_form,
        'decoration_formset': decoration_formset,
        'imprisonment_formset': imprisonment_formset,
        'soldier': soldier,
        'has_image': has_image,
        'image_url': image_url
    }
    return render(request, 'cmp/edit-soldiers.html', context)


def search_acknowledgement(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        acknowledgements = Acknowledgement.objects.filter(surname__icontains=query).order_by('surname')
    else:
        acknowledgements = Acknowledgement.objects.all().order_by('surname')
    paginator = Paginator(acknowledgements, settings.PAGE_SIZE) 
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-acknowledgement.html', {'page_obj': page_obj,  'query': query})


def search_ranks(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        ranks = Rank.objects.filter(name__icontains=query).order_by('name')
    else:
        ranks = Rank.objects.all().order_by('name')
    paginator = Paginator(ranks, settings.PAGE_SIZE) 
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-ranks.html', {'page_obj': page_obj})


def search_cemeteries(request):
    query = request.GET.get('q')
    if query:
        cemeteries = Cemetery.objects.filter(name__icontains=query).order_by('name')
    else:
        cemeteries = Cemetery.objects.all().order_by('name')
    paginator = Paginator(cemeteries, settings.PAGE_SIZE) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-cemeteries.html', {'page_obj': page_obj})


def search_powcamps(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        powcamps = PowCamp.objects.filter(name__icontains=query).order_by('name')
    else:
        powcamps = PowCamp.objects.all().order_by('name')
    paginator = Paginator(powcamps, settings.PAGE_SIZE)  # Show 10 powcamps per page
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-pow-camps.html', {'page_obj': page_obj})


def search_soldiers(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        soldiers = Soldier.objects.filter(
            Q(surname__icontains=query) |
            Q(army_number__icontains=query)
        ).order_by('surname', 'initials')
    else:
        soldiers = Soldier.objects.all().order_by('surname', 'initials')
    paginator = Paginator(soldiers, settings.PAGE_SIZE)
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-soldiers.html', {'page_obj': page_obj})


def search_decorations(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        decorations = Decoration.objects.filter(name__icontains=query).order_by('name')
    else:
        decorations = Decoration.objects.all().order_by('name')
    paginator = Paginator(decorations, settings.PAGE_SIZE)
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-decorations.html', {'page_obj': page_obj})


def search_companies(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        companies = Company.objects.filter(name__icontains=query).order_by('name')
    else:
        companies = Company.objects.all().order_by('name')
    paginator = Paginator(companies, settings.PAGE_SIZE)
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-companies.html', {'page_obj': page_obj})


def search_countries(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    if query:
        countries = Country.objects.filter(name__icontains=query).order_by('name')
    else:
        countries = Country.objects.all().order_by('name')
    paginator = Paginator(countries, settings.PAGE_SIZE) 
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/search-countries.html', {'page_obj': page_obj})
    

def detail_acknowledgement(request, acknowledgement_id):
    # get or return a 404
    rank = get_object_or_404(Rank, pk=rank_id)
    return render(request, "cmp/detail-ranks.html", {"rank": rank})


def detail_ranks(request, rank_id):
    # get or return a 404
    rank = get_object_or_404(Rank, pk=rank_id)
    return render(request, "cmp/detail-ranks.html", {"rank": rank})


def detail_powcamps(request, powcamp_id):
    # get or return a 404
    camp = get_object_or_404(Rank, pk=powcamp_id)
    return render(request, "cmp/detail-prisoner-of-war-camps.html", {"camp": camp})


def detail_cemeteries(request, cemetery_id):
    # get or return a 404
    rank = get_object_or_404(Cemetery, pk=cemetery_id)
    return render(request, "cmp/detail-cemeteries.html", {"cemetery": cemetery})


def detail_countries(request, country_id):
    # get or return a 404
    country = get_object_or_404(Country, pk=country_id)
    return render(request, "cmp/detail-countries.html", {"country": country})


def detail_companies(request, company_id):
    # get or return a 404
    company = get_object_or_404(Company, pk=company_id)
    return render(request, "cmp/detail-companies.html", {"company": company})


def detail_decorations(request, decoration_id):
    # get or return a 404
    decoration = get_object_or_404(Decoration, pk=decoration_id)
    return render(request, "cmp/detail-decorations.html", {"decoration": decoration})


def detail_soldiers(request, id):
    # get or return a 404
    soldier = get_object_or_404(Soldier, pk=id)
    return render(request, "cmp/detail-soldiers.html", {"soldier": soldier})


def edit_ranks(request, id=None):
    if id:
        rank = get_object_or_404(Rank, id=id)
        if request.method == 'POST':
            form = editRankForm(request.POST, instance=rank)
        else:
            form = editRankForm(instance=rank)
    else:
        rank = None
        form = editRankForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        rank = form.save()
        messages.success(request, f'Rank "{rank.name}" successfully {"updated" if id else "added"}!')
        return redirect('search-ranks')

    return render(request, 'cmp/edit-ranks.html', {
        'form': form,
        'rank': rank
    })


def edit_acknowledgement(request, id=None):
    print(f"Debug - Received ID: {id}")
    print(f"Debug - Request method: {request.method}")
    
    if id:
        acknowledgement = get_object_or_404(Acknowledgement, id=id)
        print(f"Debug - Found acknowledgement: {acknowledgement.id}")
        if request.method == 'POST':
            form = AcknowledgementForm(request.POST, instance=acknowledgement)
            print("Debug - Created form with POST data and instance")
        else:
            form = AcknowledgementForm(instance=acknowledgement)
            print("Debug - Created form with instance only")
    else:
        form = AcknowledgementForm(request.POST or None)
        print("Debug - Created new form without instance")
    
    if request.method == 'POST' and form.is_valid():
        acknowledgement = form.save()
        print(f"Debug - Saved form with ID: {acknowledgement.id}")
        action = "updated" if id else "added"
        messages.success(
            request, 
            f'Acknowledgement for {acknowledgement.surname}, {acknowledgement.name} successfully {action}!'
        )
        return redirect('search-acknowledgement')
    
    return render(request, "cmp/edit-acknowledgement.html", {"form": form})


def edit_cemeteries(request, id=None):
    if id:
        cemetery = get_object_or_404(Cemetery, id=id)
        if request.method == 'POST':
            form = editCemeteryForm(request.POST, instance=cemetery)
        else:
            form = editCemeteryForm(instance=cemetery)
    else:
        cemetery = None
        form = editCemeteryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        cemetery = form.save()
        messages.success(request, f'Cemetery "{cemetery.name}" successfully {"updated" if id else "added"}!')
        return redirect('search-cemeteries')

    return render(request, 'cmp/edit-cemeteries.html', {
        'form': form,
        'cemetery': cemetery
    })


def soldier(request, soldier_id):
    # get or return a 404
    soldier = get_object_or_404(Soldier, pk=soldier_id)

    # Soldier Decorations
    soldierdecorations = SoldierDecoration.objects.filter(soldier=soldier)

    # Soldier Deaths
    cemetery_map = None
    try:
        soldierdeath = SoldierDeath.objects.get(soldier=soldier)
        if soldierdeath and soldierdeath.cemetery:  # Add this check
            coordinates = [soldierdeath.cemetery.latitude, soldierdeath.cemetery.longitude]
            m = folium.Map(coordinates, zoom_start=15)
            test = folium.Html('<b>Hello world</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            marker = folium.Marker(
                location=coordinates,
                icon=folium.Icon(color='red', icon='info-sign')
            )
            marker.add_to(m)
            cemetery_map = m._repr_html_()
    except SoldierDeath.DoesNotExist:
        soldierdeath = None

    context = {
        "soldier": soldier, 
        "soldierdecorations": soldierdecorations,
        "soldierdeath": soldierdeath,
        "cemetery_map": cemetery_map
    }
    return render(request, "cmp/soldier.html", context)


def index(request):
    if request.method == 'POST':
        surname = request.POST.get('name', '')
    else:
        surname = request.GET.get('name', '')

    soldiers = Soldier.objects.filter(
        Q(surname__icontains=surname) |
        Q(army_number__icontains=surname)
    ).order_by('surname')
    paginator = Paginator(soldiers, 10)  # 10 items per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    cmp_soldier_count = Soldier.objects.count()  # Get the total count of Soldier entries
    cmp_casualty_count = SoldierDeath.objects.count()  # Get the total count of Soldier entries
    cmp_cemetery_count = Cemetery.objects.count()  # Get the total count of Soldier entries
    cmp_country_count = Cemetery.objects.count()  # Get the total count of Soldier entries
    cmp_country_count = Cemetery.objects.values('country').distinct().count()
    cmp_decoration_count = SoldierDecoration.objects.count()
    cmp_prisoner_count = SoldierImprisonment.objects.count()

    context = {
        'page_obj': page_obj,
        'surname': surname,
        'cmp_soldier_count': cmp_soldier_count,
        'cmp_casualty_count': cmp_casualty_count,
        'cmp_cemetery_count': cmp_cemetery_count,
        'cmp_country_count': cmp_country_count,
        'cmp_prisoner_count': cmp_prisoner_count,
        'cmp_decoration_count': cmp_decoration_count
    }
    return render(request, 'cmp/soldier-results.html', context)


from django.shortcuts import render, redirect
from .forms import ProvostOfficerForm, ProvostAppointmentForm

def create_provost_officer(request):
    if request.method == 'POST':
        officer_form = ProvostOfficerForm(request.POST)
        
        # Initialize formsets with POST data but no instance yet
        appointment_formset = ProvostAppointmentFormSetWithHelper(request.POST)
        decoration_formset = SoldierDecorationFormSetWithHelper(request.POST)
        
        if officer_form.is_valid() and appointment_formset.is_valid() and decoration_formset.is_valid():
            # Save the soldier first
            soldier = officer_form.save(commit=False)
            soldier.provost_officer = True
            soldier.save()
            
            # Save the appointment formset with the soldier reference
            appointment_formset.instance = soldier
            appointment_formset.save()
            
            # Save the decoration formset with the soldier reference
            decoration_formset.instance = soldier
            decoration_formset.save()
            
            messages.success(request, f'Provost Officer {soldier.surname}, {soldier.initials} successfully added')
            return redirect('provost-officer-search')
            
        # If forms are invalid, print errors for debugging
        print("Officer form errors:", officer_form.errors)
        print("Appointment formset errors:", appointment_formset.errors)
        print("Decoration formset errors:", decoration_formset.errors)
    else:
        officer_form = ProvostOfficerForm()
        appointment_formset = ProvostAppointmentFormSetWithHelper()
        decoration_formset = SoldierDecorationFormSetWithHelper()

    return render(request, 'cmp/create-provost-officer.html', {
        'officer_form': officer_form,
        'appointment_formset': appointment_formset,
        'decoration_formset': decoration_formset,
    })

def delete_acknowledgement(request, pk):
    acknowledgement = get_object_or_404(Acknowledgement, pk=pk)
    surname = acknowledgement.surname
    name = acknowledgement.name
    acknowledgement.delete()
    messages.success(request, f'Acknowledgement for {surname}, {name} successfully deleted!')
    return redirect('search-acknowledgement')

def delete_cemetery(request, id):
    cemetery = get_object_or_404(Cemetery, id=id)
    name = cemetery.name  # Store the name before deletion
    cemetery.delete()
    messages.success(request, f'Cemetery "{name}" successfully deleted!')
    return redirect('search-cemeteries')

def delete_company(request, id):
    company = get_object_or_404(Company, id=id)
    name = company.name  # Store the name before deletion
    company.delete()
    messages.success(request, f'Company "{name}" successfully deleted!')
    return redirect('search-companies')

def delete_decoration(request, id):
    decoration = get_object_or_404(Decoration, id=id)
    name = decoration.name  # Store the name before deletion
    decoration.delete()
    messages.success(request, f'Decoration "{name}" successfully deleted!')
    return redirect('search-decorations')

def delete_rank(request, id):
    rank = get_object_or_404(Rank, id=id)
    name = rank.name  # Store the name before deletion
    rank.delete()
    messages.success(request, f'Rank "{name}" successfully deleted!')
    return redirect('search-ranks')

def edit_prisoner_of_war_camps(request, id=None):
    if id:
        powcamp = get_object_or_404(PowCamp, id=id)
        if request.method == 'POST':
            form = editPrisonerOfWarCampForm(request.POST, instance=powcamp)
        else:
            form = editPrisonerOfWarCampForm(instance=powcamp)
    else:
        powcamp = None
        form = editPrisonerOfWarCampForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        powcamp = form.save()
        messages.success(request, f'PoW Camp "{powcamp.name}" successfully {"updated" if id else "added"}!')
        return redirect('search-prisoner-of-war-camps')

    return render(request, 'cmp/edit-prisoner-of-war-camps.html', {
        'form': form,
        'powcamp': powcamp
    })

def delete_prisoner_of_war_camp(request, id):
    powcamp = get_object_or_404(PrisonerOfWarCamp, id=id)
    name = powcamp.name  # Store the name before deletion
    powcamp.delete()
    messages.success(request, f'PoW Camp "{name}" successfully deleted!')
    return redirect('search-prisoner-of-war-camps')

def delete_powcamp(request, id):
    powcamp = get_object_or_404(PowCamp, id=id)
    name = powcamp.name  # Store the name before deletion
    powcamp.delete()
    messages.success(request, f'PoW Camp "{name}" successfully deleted!')
    return redirect('search-powcamps')


def delete_soldier(request, id):
    soldier = get_object_or_404(Soldier, id=id)
    name = f"{soldier.surname}, {soldier.initials}"  # Store the name before deletion
    soldier.delete()
    messages.success(request, f'Soldier "{name}" successfully deleted!')
    return redirect('search-soldiers')

def soldier_edit(request, pk):
    soldier = get_object_or_404(Soldier, pk=pk)
    if request.method == 'POST':
        form = SoldierForm(request.POST, instance=soldier)
        imprisonment_formset = SoldierImprisonmentInlineFormSet(
            request.POST,
            instance=soldier,
            prefix='imprisonment'
        )
        if form.is_valid() and imprisonment_formset.is_valid():
            form.save()
            imprisonment_formset.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = SoldierForm(instance=soldier)
        imprisonment_formset = SoldierImprisonmentInlineFormSet(
            instance=soldier,
            prefix='imprisonment'
        )
    return render(request, 'cmp/edit-soldier.html', {
        'form': form,
        'imprisonment_formset': imprisonment_formset,
        'soldier': soldier
    })

def about(request):
    return render(request, 'cmp/about.html')

def war_diaries(request):
    return render(request, 'cmp/war-diaries.html')

def ww1_diaries(request):
    return render(request, 'cmp/ww1-diaries.html')

def ww2_diaries(request):
    return render(request, 'cmp/ww2-diaries.html')

def decorations_report(request):
    # Get top 10 soldiers with most decorations
    soldiers_with_decorations = Soldier.objects.annotate(
        decoration_count=Count('soldierdecoration')
    ).filter(
        decoration_count__gt=0
    ).order_by('-decoration_count')[:10]

    context = {
        'soldiers': soldiers_with_decorations
    }
    return render(request, 'cmp/decorations-report.html', context)

def countries_report(request):
    # Get total deaths count
    total_deaths = SoldierDeath.objects.count()
    
    # Get top 10 countries by death count
    countries_with_deaths = SoldierDeath.objects.values(
        'cemetery__country__name'
    ).annotate(
        death_count=Count('id')
    ).annotate(
        percentage=Cast('death_count', FloatField()) * 100.0 / total_deaths
    ).filter(
        cemetery__country__name__isnull=False
    ).order_by('-death_count')[:10]

    context = {
        'countries': countries_with_deaths,
        'total_deaths': total_deaths
    }
    return render(request, 'cmp/countries-report.html', context)

def year_report(request):
    # Get total deaths count
    total_deaths = SoldierDeath.objects.count()
    
    # Get top 20 years by death count (changed from 10 to 20)
    years_with_deaths = SoldierDeath.objects.annotate(
        death_year=ExtractYear('date')
    ).values(
        'death_year'
    ).annotate(
        death_count=Count('id')
    ).annotate(
        percentage=Cast('death_count', FloatField()) * 100.0 / total_deaths
    ).filter(
        death_year__isnull=False
    ).order_by('-death_count')[:20]  # Changed from 10 to 20

    context = {
        'years': years_with_deaths,
        'total_deaths': total_deaths
    }
    return render(request, 'cmp/year-report.html', context)

def decorations_common(request):
    decorations = (
        Decoration.objects
        .annotate(count=Count('soldierdecoration'))
        .order_by('-count')[:20] )
    return render(request, 'cmp/decorations-common.html', { 'decorations': decorations })

def provost_officer_search(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page')
    
    # Base queryset - only get provost officers
    officers = Soldier.objects.filter(provost_officer=True)
    
    # Apply search if query exists
    if query:
        officers = officers.filter(
            Q(surname__icontains=query) |
            Q(army_number__icontains=query) |
            Q(initials__icontains=query)
        )
    
    # Order results
    officers = officers.order_by('surname', 'initials')
    
    # Paginate results
    paginator = Paginator(officers, settings.PAGE_SIZE)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'cmp/search-provost-officers.html', {
        'page_obj': page_obj,
        'query': query
    })

def provost_officer_list(request):
    officers = Soldier.objects.filter(provost_officer=True).order_by('surname', 'initials')
    paginator = Paginator(officers, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cmp/list-provost-officers.html', {'page_obj': page_obj})

def provost_officer_edit(request, id):
    officer = get_object_or_404(Soldier, id=id, provost_officer=True)
    
    if request.method == 'POST':
        officer_form = ProvostOfficerForm(request.POST, instance=officer)
        appointment_formset = ProvostAppointmentFormSetWithHelper(request.POST, instance=officer)
        decoration_formset = SoldierDecorationFormSetWithHelper(request.POST, instance=officer)
        
        if officer_form.is_valid() and appointment_formset.is_valid() and decoration_formset.is_valid():
            officer = officer_form.save()
            appointment_formset.save()
            decoration_formset.save()
            
            messages.success(request, f'Provost Officer {officer.surname}, {officer.initials} successfully updated')
            return redirect('provost-officer-search')
            
        # Print form errors for debugging
        print("Officer form errors:", officer_form.errors)
        print("Appointment formset errors:", appointment_formset.errors)
        print("Decoration formset errors:", decoration_formset.errors)
    else:
        officer_form = ProvostOfficerForm(instance=officer)
        appointment_formset = ProvostAppointmentFormSetWithHelper(instance=officer)
        decoration_formset = SoldierDecorationFormSetWithHelper(instance=officer)

    return render(request, 'cmp/edit-provost-officer.html', {
        'officer_form': officer_form,
        'appointment_formset': appointment_formset,
        'decoration_formset': decoration_formset,
        'officer': officer
    })

def provost_officer_delete(request, id):
    officer = get_object_or_404(Soldier, id=id, provost_officer=True)
    name = f"{officer.surname}, {officer.initials}"
    
    try:
        officer.delete()
        messages.success(request, f'Provost Officer "{name}" successfully deleted')
    except Exception as e:
        messages.error(request, f'Error deleting Provost Officer "{name}": {str(e)}')
        
    return redirect('provost-officer-search')

def delete_provost_appointment(request, pk):
    appointment = get_object_or_404(ProvostAppointment, pk=pk)
    soldier_id = appointment.soldier.id  # Changed from officer to soldier
    appointment.delete()
    messages.success(request, 'Provost appointment deleted successfully.')
    return redirect('edit-provost-officer', id=soldier_id)  # Redirect back to the edit page

def safe_delete(request, model, pk, redirect_url):
    try:
        obj = get_object_or_404(model, pk=pk)
        name = str(obj)
        obj.delete()
        messages.success(request, f'{model.__name__} "{name}" successfully deleted!')
    except Exception as e:
        logger.error(f'Error deleting {model.__name__} {pk}: {str(e)}')
        messages.error(request, f'Error deleting {model.__name__}')
    return redirect(redirect_url)
