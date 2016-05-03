# -*- coding: cp1252 -*-

from __future__ import unicode_literals

from django.forms import Form, ModelForm, CharField, ChoiceField, DateTimeField
from django.forms import BaseModelFormSet
from activelife.models import *

class Form_ACTIVLFormTiersComplet(Form):
    # référence des objets instances des modèles à traiter
    tiers = None
    candidat = None
    recruteur = None
    gd = None
    dp = None
    fi = None
    ap = None
    experience = None
    sal_jour = None
    sal_mois = None
    sal_an = None
    ville = None
    region = None
    # champs pour le tiers
    nom = CharField(label=u'Nom de famille', max_length=100)
    prenom = CharField(label=u'Prénom', max_length=100)
    genre = ChoiceField(label=u'Genre', choices = ( (u"Femme",u"Femme"), (u"Homme",u"Homme"), (u"Non renseigné",u"Non renseigné") ))
    anniversaire = DateTimeField('Date de naissance',required=False)
    typetiers = ChoiceField(choices = ( (u"Candidat",u"Candidat"), (u"Recruteur",u"Recruteur") ) )
    # champs pour le candidat
    identPE = CharField(max_length=16)
    # champs pour le recruteur
    raisonSociale = CharField(max_length=200)
    SIRET = CharField(max_length=14)
    # champs pour les critères de métier recherché
    valeur_GD = ChoiceField(label=u'Grand domaine', choices=getFieldChoicesROME__(ROMEGD))
    valeur_DP = ChoiceField(label=u'Domaine professionnel', choices=getFieldChoicesROME__(ROMEDP))
    valeur_Fi = ChoiceField(label=u'Fiche ROME', choices=getFieldChoicesROME__(ROMEFi))
    valeur_Ap = ChoiceField(label=u'Appellation OGR', choices=getFieldChoicesROME__(ROMEAp))
    # champs pour les autres critères recherchés
    valeur_experience = IntegerField(required=False)
    valeur_sal_jour = DecimalField(max_digits=100, decimal_places=2, required=False)
    valeur_sal_mois = DecimalField(max_digits=100, decimal_places=2, required=False)
    valeur_sal_an = DecimalField(max_digits=100, decimal_places=2, required=False)
    valeur_ville = CharField(max_digits=100, required=False)
    valeur_region = CharField(max_digits=100, required=False)
    def chargerObjetsTiers(self,tiers_id):
        # crée le tiers et toutes les instances des modèles associés, ou récupère les objets pour un tiers existant
        # renvoie l'instance du modèle tiers, liée aux instances dans les autres modèles
        self.typetiersCharge = u""
        if tiers_id == 0:
            # tiers nouveau :
            self.tiers = ACTIVLTiers()
            self.candidat = ACTIVLCandidat()
            self.recruteur = ACTIVLRecruteur()
            self.gd = ACTIVLCritMetierROMEGD()
            self.dp = ACTIVLCritMetierROMEDP()
            self.fi = ACTIVLCritMetierROMEFi()
            self.ap = ACTIVLCritMetierROMEAp()
            self.experience = ACTIVLCritExperience()
            self.sal_jour = ACTIVLCritSalaireJour()
            self.sal_mois = ACTIVLCritSalaireMois()
            self.sal_an = ACTIVLCritSalaireAn()
            self.ville = ACTIVLCritVille()
            self.region = ACTIVLCritRegion()
        else:
            # tiers existant :
            self.erreurChargementObjets = {}
            try:
                self.tiers = ACTIVLTiers.objects.get(pk=tiers_id)
                if self.tiers.typetiers in (u"Candidat",u"Recruteur"):
                    self.typetiersCharge = self.tiers.typetiers
                    self.fields['typetiers'].disabled = True # Le template va aussi s'en occuper, car pour l'instant mettre cet attribut à True ne fait rien.
                    # Mais ça servira à la vue, pour gérer les erreurs
                    print "[ACTIVELIFE] Remove field typetiers from tiers form"
                    # Render form field not editable, since typetiers had already been saved in the database
            except (KeyError, ACTIVLTiers.DoesNotExist):
                self.tiers = ACTIVLTiers()
                self.erreurChargementObjets[ACTIVLTiers] = 1
            if self.typetiersCharge != u"Recruteur":
                try:
                    self.candidat = ACTIVLCandidat.objects.filter(tiers_id=tiers_id)[0]
                except (IndexError):
                    self.candidat = ACTIVLCandidat()
                    self.erreurChargementObjets[ACTIVLCandidat] = 1
            if self.typetiersCharge != u"Candidat":
                try:
                    self.recruteur = ACTIVLRecruteur.objects.filter(tiers_id=tiers_id)[0]
                except (IndexError):
                    self.recruteur = ACTIVLRecruteur()
                    self.erreurChargementObjets[ACTIVLRecruteur] = 1
            try:
                self.gd = ACTIVLCritMetierROMEGD.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.gd = ACTIVLCritMetierROMEGD()
            try:
                self.dp = ACTIVLCritMetierROMEDP.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.dp = ACTIVLCritMetierROMEDP()
            try:
                self.fi = ACTIVLCritMetierROMEFi.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.fi = ACTIVLCritMetierROMEFi()
            try:
                self.ap = ACTIVLCritMetierROMEAp.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.ap = ACTIVLCritMetierROMEAp()
            try:
                self.experience = ACTIVLCritExperience.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.experience = ACTIVLCritExperience()
            try:
                self.sal_jour = ACTIVLCritSalaireJour.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.sal_jour = ACTIVLCritSalaireJour()
            try:
                self.sal_mois = ACTIVLCritSalaireMois.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.sal_mois = ACTIVLCritSalaireMois()
            try:
                self.sal_an = ACTIVLCritSalaireAn.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.sal_an = ACTIVLCritSalaireAn()
            try:
                self.ville = ACTIVLCritVille.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.ville = ACTIVLCritVille()
            try:
                self.region = ACTIVLCritRegion.objects.filter(tiers_id=tiers_id)[0]
            except (IndexError):
                self.region = ACTIVLCritRegion()
        # tiers nouveau ou existant :
        self.modelTuple = [self.tiers]
        if self.typetiersCharge != u"Recruteur":
            self.modelTuple += [self.candidat]
        if self.typetiersCharge != u"Candidat":
            self.modelTuple += [self.recruteur]
        self.modelTuple += [self.gd,self.dp,self.fi,self.ap,
                            self.experience,self.sal_jour,self.sal_mois,self.sal_an,self.ville,self.region]
    def preremplirChampsTiers(self):
        initialDict = {}
        initialDict['nom'] = self.tiers.nom
        initialDict['prenom'] = self.tiers.prenom
        initialDict['genre'] = self.tiers.genre
        initialDict['anniversaire'] = self.tiers.anniversaire
        # the field typetiers, if already set in the model Tiers, will be displayed as text in the template itself.
        if self.typetiersCharge == u"Candidat":
            initialDict['identPE'] = self.candidat.identPE
        if self.typetiersCharge == u"Recruteur":
            initialDict['raisonSociale'] = self.recruteur.raisonSociale
            initialDict['SIRET'] = self.recruteur.SIRET
        initialDict['valeur_GD'] = self.gd.valeur
        initialDict['valeur_DP'] = self.dp.valeur
        initialDict['valeur_Fi'] = self.fi.valeur
        initialDict['valeur_Ap'] = self.ap.valeur
        initialDict['valeur_experience'] = self.experience.valeur
        initialDict['valeur_sal_jour'] = self.sal_jour.valeur
        initialDict['valeur_sal_mois'] = self.sal_mois.valeur
        initialDict['valeur_sal_an'] = self.sal_an.valeur
        initialDict['valeur_ville'] = self.ville.valeur
        initialDict['valeur_region'] = self.region.valeur
        super(Form_ACTIVLFormTiersComplet,self).__init__(initial=initialDict)
    def sauverObjetsTiers(self,tiers_id):
        print u"[ACTIVELIFE] Form Tiers cleaned_data " + u" " + self.cleaned_data['nom'] + u" " + self.cleaned_data['prenom']
        self.tiers.nom = self.cleaned_data['nom']
        self.tiers.prenom = self.cleaned_data['prenom']
        self.tiers.genre = self.cleaned_data['genre']
        self.tiers.anniversaire = self.cleaned_data['anniversaire']
        if self.typetiersCharge not in (u"Candidat",u"Recruteur"):
            self.tiers.typetiers = self.cleaned_data['typetiers']
        if self.tiers.typetiers == u"Candidat":
            self.candidat.identPE = self.cleaned_data['identPE']
            if self.typetiersCharge not in (u"Candidat",u"Recruteur"):
                self.modelTuple.remove(self.recruteur)
                # self.recruteur.delete() #  Pas besoin : d'abord, pas sauvé, donc pas nécessaire, et en plus pas encore d'id et le delete sera alors impossible
        if self.tiers.typetiers == u"Recruteur":
            self.recruteur.raisonSociale = self.cleaned_data['raisonSociale']
            self.recruteur.SIRET = self.cleaned_data['SIRET']
            if self.typetiersCharge not in (u"Candidat",u"Recruteur"):
                self.modelTuple.remove(self.candidat)
                # self.candidat.delete() #  Pas besoin : d'abord, pas sauvé, donc pas nécessaire, et en plus pas encore d'id et le delete sera alors impossible
        self.gd.valeur = self.cleaned_data['valeur_GD']
        self.dp.valeur = self.cleaned_data['valeur_DP']
        self.fi.valeur = self.cleaned_data['valeur_Fi']
        self.ap.valeur = self.cleaned_data['valeur_Ap']
        self.dp.parent = self.gd
        self.fi.parent = self.dp
        self.ap.parent = self.fi
        self.experience.valeur = self.cleaned_data['valeur_experience']
        self.sal_jour.valeur = self.cleaned_data['valeur_sal_jour']
        self.sal_mois.valeur = self.cleaned_data['valeur_sal_mois']
        self.sal_an.valeur = self.cleaned_data['valeur_sal_an']
        self.ville.valeur = self.cleaned_data['valeur_ville']
        self.region.valeur = self.cleaned_data['valeur_region']
        self.tiers.save()
        for o in self.modelTuple[1:]:
            if tiers_id == 0 or o.__class__ in self.erreurChargementObjets:
                o.tiers = self.tiers
                print u"[ACTIVELIFE] Relié " + o.__class__.__name__ + u" au tiers " + o.tiers.__unicode__()
            o.save()
            print u"[ACTIVELIFE] " + o.__class__.__name__ + u" %i" % o.id
        return self.modelTuple

