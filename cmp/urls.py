from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


from .views import soldier_detail


urlpatterns = [
    # ... your other URL patterns ...

    path("", views.index, name="index"), 
    path('soldier/<int:soldier_id>/', views.soldier, name='soldier'),

    path("sentry-debug/", views.trigger_error ),

    path("tools/army-number-search", views.army_number_search, name="army-number-search" ),
    path("tools/army-number-search/<int:army_number>"  , views.original_unit, name="army-number-search" ),

    # Segment URLs
    path('countries/', views.countries, name='countries'),
    path('cemeteries/', views.cemeteries, name='cemeteries'),
    path('pow-camps/', views.powcamps, name='powcamps'),
    path('ranks/', views.ranks, name='ranks'),
    path('acknowledgements/', views.acknowledgements, name='acknowledgements'),

    # Mangagement URLs
    # create an index page for mgmt urls to link to /mgmt/countries
    path('mgmt/', views.mgmt_index, name='mgmt-index'),

    # Countries
    path("mgmt/countries", views.edit_countries, name="edit-countries"),
    path("mgmt/countries/<int:country_id>/", views.detail_countries, name="countries"),
    path("mgmt/countries/edit/<int:country_id>", views.edit_countries, name="edit-countries"),
    path("mgmt/countries/search/", views.search_countries, name='search-countries'),

    # Companies
    path("mgmt/companies", views.edit_companies, name="edit-companies"),
    path("mgmt/companies/<int:id>/", views.detail_companies, name="companies"),
    path("mgmt/companies/edit/<int:id>/", views.edit_companies, name='edit-companies'),
    path("mgmt/companies/search/", views.search_companies, name='search-companies'),
    path('mgmt/companies/delete/<int:id>/', views.delete_company, name='delete-company'),

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
    path("mgmt/prisoner-of-war-camps", views.edit_powcamps, name="edit-powcamps"),
    path("mgmt/prisoner-of-war-camps/<int:powcamp_id>/", views.detail_powcamps, name="powcamps"),
    path("mgmt/prisoner-of-war-camps/edit/<int:powcamp_id>", views.edit_powcamps, name="edit-prisoner-of-war-camps"),
    path("mgmt/prisoner-of-war-camps/search/", views.search_powcamps, name='search-prisoner-of-war-camps'),

    # Ranks
    path("mgmt/ranks/search/", views.search_ranks, name='search-ranks'),
    path("mgmt/ranks/edit/<int:id>/", views.edit_ranks, name='edit-ranks'),
    path("mgmt/ranks/edit/", views.edit_ranks, name='add-rank'),
    path("mgmt/ranks/delete/<int:id>/", views.delete_rank, name='delete-rank'),
    path("mgmt/ranks/<int:id>/", views.detail_ranks, name="ranks"),

    #  Acknowledgements
    path("mgmt/acknowledgement/<int:acknowledgement_id>/", views.detail_acknowledgement, name="acknowledgement"),
    path('mgmt/acknowledgement/delete/<int:pk>/', views.delete_acknowledgement, name='delete-acknowledgement'),
    path('mgmt/acknowledgement/search/', views.search_acknowledgement, name='search-acknowledgement'),
    path('mgmt/acknowledgement/edit/', views.edit_acknowledgement, name='edit-acknowledgement'),
    path('mgmt/acknowledgement/edit/<int:id>/', views.edit_acknowledgement, name='edit-acknowledgement'),


    # Provost Officers
    path('mgmt/create-provost-officer/', views.create_provost_officer, name='create-provost-officer'),

    # Soldiers
    path('soldiers/', views.soldiers, name='soldiers'),

    # Soldier management
    path("mgmt/soldiers", views.edit_soldiers, name="soldiersa"),
    path("mgmt/soldiers/<int:soldier_id>/", views.detail_soldiers, name="soldiersb"),
    path("mgmt/soldiers/edit/<int:soldier_id>", views.edit_soldiers, name="edit-soldiers"),
    path('mgmt/soldiers/search/', views.search_soldiers, name='search-soldiers'),


    #path("soldier-search/", views.soldier_search, name="soldier-search" ),
    #path("soldier-search/<str:surname>"  , views.soldier_search , name="soldier-search" ),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)