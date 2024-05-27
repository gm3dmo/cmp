from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


from .views import soldier_detail



urlpatterns = [

    #path('soldier/<int:soldier_id>/', soldier_detail, name='soldier_detail'),
    path('soldier/<int:soldier_id>/', views.soldier, name='soldier'),

    path("", views.index, name="index"), 

    path("sentry-debug/", views.trigger_error ),

    path("tools/army-number-search", views.army_number_search, name="army-number-search" ),
    path("tools/army-number-search/<int:army_number>"  , views.original_unit, name="army-number-search" ),

    # Segment URLs
    path('countries/', views.countries, name='countries'),
    path('cemeteries/', views.cemeteries, name='cemeteries'),
    path('pow-camps/', views.powcamps, name='powcamps'),

    path('ranks/', views.ranks, name='ranks'),

    # Mangagement URLs
    # create an index page for mgmt urls to link to /mgmt/countries
    path('mgmt/', views.mgmt_index, name='mgmt-index'),

    # Countries
    path("mgmt/countries", views.edit_countries, name="edit-countries"),
    path("mgmt/countries/<int:country_id>/", views.detail_countries, name="countries"),
    path("mgmt/countries/edit/<int:country_id>", views.edit_countries, name="edit-countries"),
    path("mgmt/countries/search/", views.search_countries, name='search-countries'),

    # Cemeteries 
    path("mgmt/cemeteries", views.edit_cemeteries, name="edit-cemeteries"),
    path("mgmt/cemeteries/<int:cemetery_id>/", views.detail_cemeteries, name="cemeteries"),
    path("mgmt/cemeteries/edit/<int:cemetery_id>", views.edit_cemeteries, name="edit-cemeteries"),
    path("mgmt/cemeteries/search/", views.search_cemeteries, name='search-cemeteries'),

    # POW Camps
    path("mgmt/prisoner-of-war-camps", views.edit_powcamps, name="edit-powcamps"),
    path("mgmt/prisoner-of-war-camps/<int:powcamp_id>/", views.detail_powcamps, name="powcamps"),
    path("mgmt/prisoner-of-war-camps/edit/<int:powcamp_id>", views.edit_powcamps, name="edit-prisoner-of-war-camps"),
    path("mgmt/prisoner-of-war-camps/search/", views.search_powcamps, name='search-prisoner-of-war-camps'),

    # Ranks
    path("mgmt/ranks", views.edit_ranks, name="edit-ranks"),
    path("mgmt/ranks/<int:rank_id>/", views.detail_ranks, name="ranks"),
    path("mgmt/ranks/edit/<int:rank_id>", views.edit_ranks, name="edit-ranks"),
    path('mgmt/ranks/search/', views.search_ranks, name='search-ranks'),


    # Soldiers
    path('soldiers/', views.soldiers, name='soldiers'),

    # Soldier management
    path("mgmt/soldiers", views.edit_soldiers, name="soldiers"),
    path("mgmt/soldiers/<int:soldier_id>/", views.detail_soldiers, name="soldiers"),
    path("mgmt/soldiers/edit/<int:soldier_id>", views.edit_soldiers, name="edit-soldiers"),
    path('mgmt/soldiers/search/', views.search_soldiers, name='search-soldiers'),

    

    #path("soldier-search/", views.soldier_search, name="soldier-search" ),
    #path("soldier-search/<str:surname>"  , views.soldier_search , name="soldier-search" ),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)