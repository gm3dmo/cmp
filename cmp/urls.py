from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

# ...


urlpatterns = [

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
    path("mgmt/countries", views.edit_countries, name="countries"),
    path("mgmt/countries/<int:country_id>/", views.detail_countries, name="countries"),
    path("mgmt/countries/edit/<int:country_id>", views.edit_countries, name="edit-countries"),

    path("mgmt/ranks", views.edit_ranks, name="ranks"),
    path("mgmt/pow-camps", views.edit_powcamps, name="powcamps"),
    path("mgmt/cemeteries", views.edit_cemeteries, name="cemeteries"),

    # Soldiers
    path('soldiers/', views.soldiers, name='soldiers'),
    path("mgmt/soldiers", views.edit_soldiers, name="soldiers"),
    path("mgmt/soldiers/<int:soldier_id>/", views.detail_soldiers, name="soldiers"),
    path("mgmt/soldiers/edit/<int:soldier_id>", views.edit_soldiers, name="edit-soldiers"),
    
    path('soldier/<int:soldier_id>/', views.soldier, name='soldier'),

    #path("soldier-search/", views.soldier_search, name="soldier-search" ),
    #path("soldier-search/<str:surname>"  , views.soldier_search , name="soldier-search" ),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)