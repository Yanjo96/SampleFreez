# Use include() to add paths from the blood application
from django.urls import path
from django.urls import re_path
from . import views
from django.views import generic
from django.conf.urls import url
from django.views.generic.list import ListView

urlpatterns = [
    path('', views.index, name='index'),
    #all the freezer urls
    re_path(r'^freezer/$',views.FreezerListView.as_view(), name='freezer'),
    re_path(r'^freezer/(?P<pk>\d+)/$',views.FreezerDetailView.as_view(), name='freezer-detail'),
    re_path(r'^freezer/create/$',views.FreezerCreate.as_view(),name='freezer-create'),
    re_path(r'^freezer/(?P<pk>\d+)/update/$',views.FreezerUpdate.as_view(),name='freezer-update'),
    re_path(r'^freezer/(?P<pk>\d+)/delete/$',views.FreezerDelete.as_view(),name='freezer-delete'),
    #all the compartments urls
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<pk>\d+)/$',views.CompartmentDetailView.as_view(), name='compartment-detail'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/create/$',views.CompartmentCreate.as_view(),name='compartment-create'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<pk>\d+)/update/$',views.CompartmentUpdate.as_view(),name='compartment-update'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<pk>\d+)/delete/$',views.CompartmentDelete.as_view(),name='compartment-delete'),
    #all the rack urls
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<pk>\d+)/$',views.RackDetailView.as_view(), name='rack-detail'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/create/$',views.RackCreate.as_view(),name='rack-create'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<pk>\d+)/update/$',views.RackUpdate.as_view(),name='rack-update'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<pk>\d+)/delete/$',views.RackDelete.as_view(),name='rack-delete'),
    #all the rackmodule urls
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<pk>\d+)/$',views.RackmoduleDetailView.as_view(), name='rackmodule-detail'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/create/$',views.RackmoduleCreate.as_view(),name='rackmodule-create'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<pk>\d+)/update/$',views.RackmoduleUpdate.as_view(),name='rackmodule-update'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<pk>\d+)/delete/$',views.RackmoduleDelete.as_view(),name='rackmodule-delete'),
    #all the box urls
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>\d+)/box/(?P<pk>\d+)/$',views.BoxRackDetailView.as_view(), name='box-r-detail'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>\d+)/box/create/$',views.BoxRackCreate.as_view(),name='box-r-create'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>\d+)/box/(?P<pk>\d+)/update/$',views.BoxRackUpdate.as_view(),name='box-r-update'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>\d+)/box/(?P<pk>\d+)/delete/$',views.BoxRackDelete.as_view(),name='box-r-delete'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/(?P<pk>\d+)/$',views.BoxCompartmentDetailView.as_view(), name='box-c-detail'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/create/$',views.BoxCompartmentCreate.as_view(),name='box-c-create'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/(?P<pk>\d+)/update/$',views.BoxCompartmentUpdate.as_view(),name='box-c-update'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/(?P<pk>\d+)/delete/$',views.BoxCompartmentDelete.as_view(),name='box-c-delete'),
    #all the tube urls
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>)\d+/box/(?P<box>\d+)/tube/(?P<pk>\d+)/$',views.TubeRackDetailView.as_view(),name='tube-r-detail'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>\d+)/box/(?P<box>\d+)/tube/create/$',views.TubeRackCreate.as_view(),name='tube-r-create'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>\d+)/box/(?P<box>\d+)/tube/(?P<pk>\d+)/update/$',views.TubeRackUpdate.as_view(),name='tube-r-update'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/rack/(?P<rack>\d+)/rackmodule/(?P<rackmodule>\d+)/box/(?P<box>\d+)/tube/(?P<pk>\d+)/delete/$',views.TubeRackDelete.as_view(),name='tube-r-delete'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/(?P<box>\d+)/tube/(?P<pk>\d+)/$',views.TubeCompartmentDetailView.as_view(), name='tube-c-detail'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/(?P<box>\d+)/tube/create/$',views.TubeCompartmentCreate.as_view(),name='tube-c-create'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/(?P<box>\d+)/tube/(?P<pk>\d+)/update/$',views.TubeCompartmentUpdate.as_view(),name='tube-c-update'),
    re_path(r'^freezer/(?P<freezer>\d+)/compartment/(?P<compartment>\d+)/box/(?P<box>\d+)/tube/(?P<pk>\d+)/delete/$',views.TubeCompartmentDelete.as_view(),name='tube-c-delete'),
    re_path(r'^biosample/(?P<biosample>\d+)/tube/create/$',views.TubeBiosampleCreate.as_view(),name='tube-b-create'),
    #all the biosample urls
    re_path(r'^biosample/$',views.BioSampleListView.as_view(), name='biosample'),
    re_path(r'^biosample/(?P<pk>\d+)/$',views.BioSampleDetailView.as_view(), name='biosample-detail'),
    re_path(r'^biosample/create/$',views.BioSampleCreate.as_view(),name='biosample-create'),
    re_path(r'^biosample/(?P<pk>\d+)/update/$',views.BioSampleUpdate.as_view(),name='biosample-update'),
    re_path(r'^biosample/(?P<pk>\d+)/delete/$',views.BioSampleDelete.as_view(),name='biosample-delete'),
    #all the type urls
    re_path(r'^type/$',views.TypeListView.as_view(), name='type'),
    re_path(r'^type/(?P<pk>\d+)/$',views.TypeDetailView.as_view(), name='type-detail'),
    re_path(r'^type/create/$',views.TypeCreate.as_view(),name='type-create'),
    re_path(r'^type/(?P<pk>\d+)/update/$',views.TypeUpdate.as_view(),name='type-update'),
    re_path(r'^type/(?P<pk>\d+)/delete/$',views.TypeDelete.as_view(),name='type-delete'),
    # AJAX
    path('ajax/load-compartments/', views.load_compartments, name='ajax_load_compartments'),
    path('ajax/load-racks/', views.load_racks, name='ajax_load_racks'),
    path('ajax/load-rackmodules/', views.load_rackmodules, name='ajax_load_rackmodules'),
    # Upload
    url(r'^uploads/$', views.model_form_upload, name='upload'),
    # re_path(r'^search/$', views.FreezerSearchListView.as_view(), name="freezer_search_list_view"),
    re_path(r'^search/$', views.SearchListView.as_view(), name="search_list_view"),

]
