# -*- coding: cp1252 -*-

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import *
from activelife.forms.UpdateACTIVLTiersCritMetier import *

def index(request):
    return HttpResponse(u"Index d'ACTIVELIFE.")

def TiersIndex(request):
#    try:       
    return render(request, 'activelife/tiers_index.html', {
        'candidat_list':  ACTIVLTiers.objects.filter(typetiers="Candidat"),
        'recruteur_list': ACTIVLTiers.objects.filter(typetiers="Recruteur"),
    })
#    except (Exception):
#        return HttpResponse(u"Problème technique lors du rendu de la vue TiersIndex")

def saisirTiers(request, tiers_id_):
    # convertir en int, car le paramètre venant de l'URL arrive comme chaîne Unicode, par exemple u"0"
    # et alors la comparaison de u"0" avec 0 renvoie toujours à False (unicode comparé à un numérique)
    if not isinstance( tiers_id_, ( int, long ) ):
        tiers_id = int(tiers_id_)
    else:
        tiers_id = tiers_id_
    error_message = u""
    if request.method == "POST":
        form = Form_ACTIVLFormTiersComplet(request.POST)
        form.chargerObjetsTiers(tiers_id) # charger les objets pour pouvoir les sauvegarder
        if form.is_valid():
            validationError = False
        else:
            print "[ACTIVELIFE] Nombre d'erreurs sur le formulaire Tiers : %i" % len(form.errors)
            print "[ACTIVELIFE] form.fields[ typetiers ].disabled : %i" % form.fields['typetiers'].disabled  
            for e in form.errors:
                print "[ACTIVELIFE] Erreur : " + e
            validationError = True
            skipErrors = []
            if form.fields['typetiers'].disabled == True:
                # cas où on a voulu modifier un tiers existant
                skipErrors.append(u'typetiers')
                if form.typetiersCharge == u"Candidat":
                    skipErrors.append(u'raisonSociale')
                    skipErrors.append(u'SIRET')
                if form.typetiersCharge == u"Recruteur":
                    skipErrors.append(u'identPE')
            if 'typetiers' in form.cleaned_data:
                # Si on vient de choisir le type de tiers, certains champs peuvent rester vides (ceux du type de tiers non choisi)
                if form.cleaned_data['typetiers'] == u'Candidat':
                    skipErrors.append(u'raisonSociale')
                    skipErrors.append(u'SIRET')
                if form.cleaned_data['typetiers'] == u'Recruteur':
                    skipErrors.append(u'identPE')
            for cleChamp in skipErrors:
                if cleChamp in form.errors:
                    print "[ACTIVELIFE] Delete erreur : " + cleChamp
                    del form.errors[cleChamp]
            print "[ACTIVELIFE] Nombre d'erreurs sur le formulaire Tiers : %i" % len(form.errors)
            for e in form.errors:
                print "[ACTIVELIFE] Erreur : " + e
            if len(form.errors) == 0:
                    validationError = False
        if validationError == False:
            form.sauverObjetsTiers(tiers_id) # équivalent à form.save(commit=true) pour une ModelForm
            return HttpResponseRedirect(reverse('activelife:tiers_index'))
            # Succès de la modification d'un tiers existant ou de la création d'un nouveau tiers
            # Toujours renvoyer une réponse HTTP Redirect après avoir traité avec succès une requête POST.
            # Cela évite que la requête POST soit envoyée deux fois si un utilisateur clique sur Précédent.
        else:
            error_message = u"Erreur dans les données renseignées !"
    else:
        form = Form_ACTIVLFormTiersComplet()
        if tiers_id > 0:
            form.chargerObjetsTiers(tiers_id) # charger les objets pour pouvoir pré-remplir les valeurs de champs avec celles existantes
            form.preremplirChampsTiers()
    # Création/Lecture/Modification d'un tiers
    try:
        return render(request, 'activelife/saisirTiers.html', {
            'form':  form,
            'error_message': error_message,
        })
    except (KeyError):
        return HttpResponse("Problème technique lors du rendu du tiers d'ID " + u"%i" % tiers_ID)

def getFieldChoicesROME_JSON__1(request,className):
    return HttpResponse(getFieldChoicesROME_JSON__(className))
def getFieldChoicesROME_JSON__2(request,className,letter):
    return HttpResponse(getFieldChoicesROME_JSON__(className,letter))

def getTreeForROME_JSON__0(request):
    return HttpResponse(getTreeForROME_JSON__())
def getTreeForROME_JSON__1(request,depht_):
    # convertir en int, car le paramètre venant de l'URL arrive comme chaîne Unicode, par exemple u"0"
    # et alors la comparaison de u"0" avec 0 renvoie toujours à False (unicode comparé à un numérique)
    if not isinstance( depht_, ( int, long ) ):
        depht = int(depht_)
    else:
        depht = depht_
    return HttpResponse(getTreeForROME_JSON__(depht))

def loadROMEModels_view_(request):
    loadROMEModels()
    return HttpResponse(u"Les objets de modèles pour les codes ROME ont été chargés : GD DP Fi Ap")

def loadROMEModels_view(request,level_):
    if not isinstance( level_, ( int, long ) ):
        level = int(level_)
    else:
        level = level_
    loadROMEModels(level)
    r = u"Les objets de modèles pour les codes ROME ont été chargés : "
    iLevel = level - 1000
    if iLevel >= 0:
        #niveau 1 : GD
        r += u"GD "
    else:
        iLevel = level
    iLevel = level - 100
    if iLevel >= 0:
        #niveau 2 : DP
        r += u"DP "
    else:
        iLevel = level
    iLevel = level - 10
    if iLevel >= 0:
        #niveau 3 : Fi
        r += u"Fi "
    else:
        iLevel = level
    iLevel = level - 1
    if iLevel >= 0:
        #niveau 4 : Ap
        r += u"Ap "
    else:
        iLevel = level
    return HttpResponse(r)

def connectROMEModels_view_(request):
    connectROMEModels()
    return HttpResponse(u"Les objets de modèles pour les codes ROME ont été connectés entre eux : DP_vers_GD Fi_vers_DP Ap_vers_Fi ")

def connectROMEModels_view(request,level_):
    if not isinstance( level_, ( int, long ) ):
        level = int(level_)
    else:
        level = level_
    connectROMEModels(level)
    r = u"Les objets de modèles pour les codes ROME ont été connectés entre eux : "
    iLevel = level - 100
    if iLevel >= 0:
        #niveau 1 : DP
        r += u"DP_vers_GD "
    else:
        iLevel = level
    iLevel = level - 10
    if iLevel >= 0:
        #niveau 2 : Fi
        r += u"Fi_vers_DP "
    else:
        iLevel = level
    iLevel = level - 1
    if iLevel >= 0:
        #niveau 3 : Ap
        r += u"Ap_vers_Fi "
    else:
        iLevel = level
    return HttpResponse(r)

def deleteROMEModels_view_(request):
    deleteROMEModels()
    return HttpResponse(u"Les objets de modèles pour les codes ROME ont été supprimés : GD DP Fi Ap")

def deleteROMEModels_view(request,level_):
    if not isinstance( level_, ( int, long ) ):
        level = int(level_)
    else:
        level = level_
    deleteROMEModels(level)
    r = u"Les objets de modèles pour les codes ROME ont été supprimés : "
    iLevel = level - 1000
    if iLevel >= 0:
        #niveau 1 : GD
        r += u"GD "
    else:
        iLevel = level
    iLevel = level - 100
    if iLevel >= 0:
        #niveau 2 : DP
        r += u"DP "
    else:
        iLevel = level
    iLevel = level - 10
    if iLevel >= 0:
        #niveau 3 : Fi
        r += u"Fi "
    else:
        iLevel = level
    iLevel = level - 1
    if iLevel >= 0:
        #niveau 4 : Ap
        r += u"Ap "
    else:
        iLevel = level
    return HttpResponse(r)



