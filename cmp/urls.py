from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic.base import RedirectView
import os
from django.contrib.auth.decorators import login_required


from .views import soldier_detail


def protect_patterns(patterns):
    protected = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = login_required(callback)
        protected.append(pattern)
    return protected

mgmt_patterns = [
    # Management index
    path('mgmt/', views.mgmt_index, name='mgmt-index'),

    # Countries
    path("mgmt/countries", views.edit_countries, name="edit-countries"),
    path("mgmt/countries/<int:country_id>/", views.detail_countries, name="countries"),
    path("mgmt/countries/edit/<int:country_id>", views.edit_countries, name="edit-countries"),
    path("mgmt/countries/search/", views.search_countries, name='search-countries'),

    # Decorations
    path("mgmt/decorations", views.edit_decorations, name="edit-decorations"),
    path("mgmt/decorations/<int:decoration_id>/", views.detail_decorations, name="decorations"),
    path("mgmt/decorations/edit/<int:decoration_id>", views.edit_decorations, name="edit-decorations"),
    path("mgmt/decorations/edit/", views.edit_decorations, name="add-decoration"),
    path("mgmt/decorations/search/", views.search_decorations, name='search-decorations'),
    path("mgmt/decorations/delete/<int:id>/", views.delete_decoration, name='delete-decoration'),

    # Cemeteries 
    path("mgmt/cemeteries", views.edit_cemeteries, name="edit-cemeteries"),
    path("mgmt/cemeteries/<int:cemetery_id>/", views.detail_cemeteries, name="cemeteries"),
    path("mgmt/cemeteries/edit/<int:id>/", views.edit_cemeteries, name='edit-cemetery'),
    path("mgmt/cemeteries/edit/", views.edit_cemeteries, name='add-cemetery'),
    path("mgmt/cemeteries/search/", views.search_cemeteries, name='search-cemeteries'),
    path("mgmt/cemeteries/delete/<int:id>/", views.delete_cemetery, name="delete-cemetery"),

    # POW Camps
    path("mgmt/pow-camps/search/", views.search_powcamps, name='search-powcamps'),
    path("mgmt/pow-camps/edit/<int:id>/", views.edit_powcamps, name='edit-powcamps'),
    path("mgmt/pow-camps/edit/", views.edit_powcamps, name='edit-powcamps'),
    path("mgmt/pow-camps/delete/<int:id>/", views.delete_powcamp, name='delete-powcamp'),

    # Ranks
    path("mgmt/ranks/search/", views.search_ranks, name='search-ranks'),
    path("mgmt/ranks/edit/<int:id>/", views.edit_ranks, name='edit-ranks'),
    path("mgmt/ranks/edit/", views.edit_ranks, name='add-rank'),
    path("mgmt/ranks/delete/<int:id>/", views.delete_rank, name='delete-rank'),
    path("mgmt/ranks/<int:id>/", views.detail_ranks, name="ranks"),

    # Acknowledgements
    path("mgmt/acknowledgement/<int:acknowledgement_id>/", views.detail_acknowledgement, name="acknowledgement"),
    path('mgmt/acknowledgement/delete/<int:pk>/', views.delete_acknowledgement, name='delete-acknowledgement'),
    path('mgmt/acknowledgement/search/', views.search_acknowledgement, name='search-acknowledgement'),
    path('mgmt/acknowledgement/edit/', views.edit_acknowledgement, name='edit-acknowledgement'),
    path('mgmt/acknowledgement/edit/<int:id>/', views.edit_acknowledgement, name='edit-acknowledgement'),

    # Provost Officers
    path('mgmt/provost-officers/search/', views.provost_officer_search, name='provost-officer-search'),
    path('mgmt/provost-officers/create/', views.create_provost_officer, name='create-provost-officer'),
    path('mgmt/provost-officers/edit/<int:id>/', views.provost_officer_edit, name='edit-provost-officer'),
    path('mgmt/provost-officers/delete/<int:id>/', views.provost_officer_delete, name='delete-provost-officer'),

    # Soldiers
    path("mgmt/soldiers/search/", views.search_soldiers, name='search-soldiers'),
    path("mgmt/soldiers/edit/<int:id>/", views.edit_soldier, name='edit-soldier'),
    path("mgmt/soldiers/edit/", views.edit_soldier, name='create-soldier'),
    path("mgmt/soldiers/delete/<int:id>/", views.delete_soldier, name='delete-soldier'),
    path("mgmt/soldiers/<int:id>/", views.detail_soldiers, name='detail-soldiers'),
    path('mgmt/soldiers/<int:id>/edit/', views.edit_soldier, name='edit-soldier'),

    # Companies
    path("mgmt/companies", views.edit_companies, name="edit-companies"),
    path("mgmt/companies/<int:id>/", views.detail_companies, name="companies"),
    path("mgmt/companies/edit/<int:id>/", views.edit_companies, name='edit-companies'),
    path("mgmt/companies/search/", views.search_companies, name='search-companies'),
    path('mgmt/companies/delete/<int:id>/', views.delete_company, name='delete-company'),
]

urlpatterns = [
    # ... your other URL patterns ...

    path("", views.index, name="index"), 
    path('soldier/<int:soldier_id>/', views.soldier, name='soldier'),

    path("sentry-debug/", views.trigger_error ),

    path("tools/army-number-search", views.army_number_search, name="army-number-search" ),
    path("tools/army-number-search/<int:army_number>"  , views.original_unit, name="army-number-search" ),
    path('tools/army-number-search/', views.army_number_search, name='army-number-search'),
    path('tools/armynumber/', RedirectView.as_view(pattern_name='army-number-search', permanent=True), name='tools-armynumber'),

    # Segment URLs
    path('countries/', views.countries, name='countries'),
    path('cemeteries/', views.cemeteries, name='cemeteries'),
    path('pow-camps/', views.powcamps, name='powcamps'),
    path('ranks/', views.ranks, name='ranks'),
    path('acknowledgements/', views.acknowledgements, name='acknowledgements'),

    path('ww1-diaries/', views.ww1_diaries, name='ww1-diaries'),
    path('ww2-diaries/', views.ww2_diaries, name='ww2-diaries'),

    path('accounts/', include('allauth.urls')),
    path('', include(protect_patterns(mgmt_patterns))),

    # Reports
    path('reports/decorations/', views.decorations_report, name='decorations-report'),
    path('reports/decorations/common/', views.decorations_common, name='decorations-common'),
    path('reports/countries/', views.countries_report, name='countries-report'),
    path('reports/year/', views.year_report, name='year-report'),

    # About
    path('about/', views.about, name='about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)