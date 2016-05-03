from django.conf.urls import url

from . import views

app_name="activelife"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tiers/$', views.TiersIndex, name='tiers_index'),
    url(r'^tiers/(?P<tiers_id_>[0-9]+)/$', views.saisirTiers, name='saisir_tiers'),
    url(r'^loadROMEModels/(?P<level_>[0-9]+)/$', views.loadROMEModels_view, name='loadROMEModels'),
    url(r'^loadROMEModels/$', views.loadROMEModels_view_, name='loadROMEModels_'),
    url(r'^connectROMEModels/(?P<level_>[0-9]+)/$', views.connectROMEModels_view, name='connectROMEModels'),
    url(r'^connectROMEModels/$', views.connectROMEModels_view_, name='connectROMEModels_'),
    url(r'^deleteROMEModels/(?P<level_>[0-9]+)/$', views.deleteROMEModels_view, name='deleteROMEModels'),
    url(r'^deleteROMEModels/$', views.deleteROMEModels_view_, name='deleteROMEModels_'),
    url(r'^getFieldChoicesROME_JSON__/(?P<className>ROMEGD|ROMEDP|ROMEFi|ROMEAp)/$', views.getFieldChoicesROME_JSON__1, name='getFieldChoicesROME_JSON__'),
    url(r'^getFieldChoicesROME_JSON__/(?P<className>ROMEDP)/(?P<letter>[A-Z])/$', views.getFieldChoicesROME_JSON__2, name='getFieldChoicesROME_JSON__'),
    url(r'^getFieldChoicesROME_JSON__/(?P<className>ROMEFi)/(?P<letter>[A-Z][0-9][0-9])/$', views.getFieldChoicesROME_JSON__2, name='getFieldChoicesROME_JSON__'),
    url(r'^getFieldChoicesROME_JSON__/(?P<className>ROMEAp)/(?P<letter>[A-Z][0-9][0-9][0-9][0-9])/$', views.getFieldChoicesROME_JSON__2, name='getFieldChoicesROME_JSON__'),
    url(r'^getTreeForROME_JSON__0/$', views.getTreeForROME_JSON__0, name='getTreeForROME_JSON__0'),
    url(r'^getTreeForROME_JSON__1/(?P<depht_>[1-9])/$', views.getTreeForROME_JSON__1, name='getTreeForROME_JSON__1'),
]

