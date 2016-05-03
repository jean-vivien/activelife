from django.contrib import admin

# Register your models here.

from .models import ACTIVLCandidat, ACTIVLRecruteur, ACTIVLTiers
from .models import ACTIVLCritMetierROMEGD, ACTIVLCritMetierROMEDP, ACTIVLCritMetierROMEFi, ACTIVLCritMetierROMEAp
    
class ACTIVLCritMetierROMEGDInline(admin.TabularInline):
    model = ACTIVLCritMetierROMEGD
    extra = 1
    max_num = 1
class ACTIVLCritMetierROMEDPInline(admin.TabularInline):
    model = ACTIVLCritMetierROMEDP
    extra = 1
    max_num = 1
class ACTIVLCritMetierROMEFiInline(admin.TabularInline):
    model = ACTIVLCritMetierROMEFi
    extra = 1
    max_num = 1
class ACTIVLCritMetierROMEApInline(admin.TabularInline):
    model = ACTIVLCritMetierROMEAp
    extra = 1
    max_num = 1

class ACTIVLCandidatInline(admin.TabularInline):
    model = ACTIVLCandidat
    extra = 1
    max_num = 1
class ACTIVLRecruteurInline(admin.TabularInline):
    model = ACTIVLRecruteur
    extra = 1
    max_num = 1

class ACTIVLTiersAdmin(admin.ModelAdmin):
    fieldsets = [
        (u'Coordonnees',    {'fields': ['prenom','nom','genre','anniversaire']})
    ]
    inlines = [ACTIVLCandidatInline,ACTIVLRecruteurInline,
               ACTIVLCritMetierROMEGDInline,ACTIVLCritMetierROMEDPInline,ACTIVLCritMetierROMEFiInline,ACTIVLCritMetierROMEApInline]

##class ACTIVLRecruteurAdmin(admin.ModelAdmin):
##    fieldsets = [
##        (u"Coordonnees",    {'fields': ['raisonSociale','SIRET']})
##    ]
##    inlines = [ACTIVLCritGeoInline,ACTIVLCritIdeesInline,ACTIVLCritVillePopInline,ACTIVLCritPrixM2Inline]

admin.site.register(ACTIVLTiers, ACTIVLTiersAdmin)
#admin.site.register(ACTIVLRecruteur, ACTIVLRecruteurAdmin)
#admin.site.register(Choice)
