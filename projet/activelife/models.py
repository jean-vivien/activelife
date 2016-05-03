# -*- coding: cp1252 -*-
from __future__ import unicode_literals

import datetime
import json

from django.db import models
from django.utils import timezone

from .PE_access_dataset import PE_access_dataset

def JV_letter_range(start, stop):
    for c in xrange(ord(start), ord(stop)+1):
        yield chr(c)
def JV_letter_ranges(startstoparray,strs_ = [u""]):
    if len(startstoparray) >0:
        strs = []
        for s in strs_:
            for c in xrange(ord(startstoparray[0][0]), ord(startstoparray[0][1])+1):
                strs.append(s + chr(c))
        return JV_letter_ranges(startstoparray[1:],strs)
    else:
        return strs_

# Create your models here.

class ROMEGD(models.Model):
    code = models.CharField(max_length=1)
    text = models.CharField(max_length=100)
    def __unicode__(self):
        return self.code + u" " + self.text

class ROMEDP(models.Model):
    def connect(self):
        manager = ROMEGD.objects
        found = manager.filter(code="".join([self.code[0]]))
        if len(found) < 1:
            print u"[ACTIVELIFE]" + self.__unicode__() + u" --- parent not found"
            found = manager.all()
            if len(found) < 1:
                found = [None]
        return found[0]
    def connectID(self):
        c = self.connect()
        if c is None:
            return 0
        else:
            return c.id
    code = models.CharField(max_length=3)
    text = models.CharField(max_length=100)
    parent = models.ForeignKey(ROMEGD, null=True)
    def __unicode__(self):
        return self.code + u" " + self.text

class ROMEFi(models.Model):
    def connect(self):
        manager = ROMEDP.objects
        found = manager.filter(code=self.code[0:3])
        if len(found) < 1:
            print u"[ACTIVELIFE]" + self.__unicode__() + u" --- parent not found"
            found = manager.all()
            if len(found) < 1:
                found = [None]
        return found[0]
    def connectID(self):
        c = self.connect()
        if c is None:
            return 0
        else:
            return c.id
    code = models.CharField(max_length=5)
    text = models.CharField(max_length=100)
    parent = models.ForeignKey(ROMEDP, null=True)
    def __unicode__(self):
        return self.code + u" " + self.text

class ROMEAp(models.Model):
    def connect(self):
        manager = ROMEFi.objects
        found = manager.filter(code=self.codeROME)
        if len(found) < 1:
            print u"[ACTIVELIFE]" + self.__unicode__() + u" --- parent not found"
            found = manager.all()
            if len(found) < 1:
                found = [None]
        return found[0]
    def connectID(self):
        c = self.connect()
        if c is None:
            return 0
        else:
            return c.id
    codeROME = models.CharField(max_length=5,default="?0000")
    codeOGR = models.CharField(max_length=5)
    text = models.CharField(max_length=200)
    parent = models.ForeignKey(ROMEFi, null=True)
    def __unicode__(self):
        return self.codeROME + u"->" + self.codeOGR + u" " + self.text

fieldChoicesROME__ = {ROMEGD:[],ROMEDP:[],ROMEFi:[],ROMEAp:[]}
fieldChoicesROME__byLetter = {
                              ROMEDP:{
                                        x:[] for x in JV_letter_ranges(
                                                                                    [[u'A',u'Z']])
                                     },
                              ROMEFi:{
                                        x:[] for x in JV_letter_ranges(
                                                                                    [[u'A',u'Z'],
                                                                                     [u'0',u'9'],
                                                                                     [u'0',u'9']
                                                                                    ]
                                                                                 )
                                     },
                              ROMEAp:{
                                        x:[] for x in JV_letter_ranges(
                                                                                    [[u'A',u'Z'],
                                                                                     [u'0',u'9'],
                                                                                     [u'0',u'9'],
                                                                                     [u'0',u'9'],
                                                                                     [u'0',u'9']
                                                                                    ]
                                                                                 )
                                     }
                             } # NB : ''.join(x) vaut x si x est déjà une chaîne de caractères...
def getFieldChoicesROME__(classe):
    if len(fieldChoicesROME__[classe]) == 0:
        for o in classe.objects.all():
            fieldChoicesROME__[classe].append((o.__unicode__(),o.__unicode__()))
    return fieldChoicesROME__[classe]

def getFieldChoicesROME__byLetter(classe,letter):
    mainData = fieldChoicesROME__byLetter[classe]
    dataByLetter = mainData[letter]
    if len(dataByLetter) == 0:
        for o in classe.objects.all():
            value = o.__unicode__()
            doAppend = False
            if classe == ROMEDP:
                if value[0] == letter[0]:
                    doAppend = True
            if classe == ROMEFi:
                if value[0:3] == letter[0:3]:
                    doAppend = True
            if classe == ROMEAp:
                if value[0:5] == letter[0:5]:
                    doAppend = True
            if doAppend == True:
                dataByLetter.append((value,value))
    return dataByLetter

def getFieldChoicesROME_JSON__(className,letter=u''):
    if className == u"ROMEGD":
        classParam = ROMEGD
    if className == u"ROMEDP":
        classParam = ROMEDP
    if className == u"ROMEFi":
        classParam = ROMEFi
    if className == u"ROMEAp":
        classParam = ROMEAp
    if letter == u'':
        data = getFieldChoicesROME__(classParam)
    else:
        validLetter = False
        if className == u"ROMEDP":
            if letter in JV_letter_ranges([[u'A',u'Z']]):
                validLetter = True
        if className == u"ROMEFi":
            if letter in JV_letter_ranges([[u'A',u'Z'],[u'0',u'9'],[u'0',u'9']]):
                validLetter = True
        if className == u"ROMEAp":
            if letter in JV_letter_ranges([[u'A',u'Z'],[u'0',u'9'],[u'0',u'9'],[u'0',u'9'],[u'0',u'9']]):
                validLetter = True
        if validLetter == True:
            data = getFieldChoicesROME__byLetter(classParam,letter)
        else:
            data = u"Erreur de clé !"
    return json.dumps(data)

def getTreeForROME_JSON__(depht=4):
    rootObject = {}
    rootObject[u"name"] = u"Votre métier ?"
    rootObject[u"children"] = []
    # Depht 1 - ROMEGD
    gdList = getFieldChoicesROME__(ROMEGD)
    for gd in gdList:
        gdChild = {}
        gdChild[u"name"] = gd[0]
        rootObject[u"children"].append(gdChild)
        if depht > 1 :
            gdChild[u"children"] = []
            # Depht 2 - ROMEDP
            dpList = getFieldChoicesROME__byLetter(ROMEDP,gd[0][0])
            for dp in dpList:
                dpChild = {}
                dpChild[u"name"] = dp[0]
                gdChild[u"children"].append(dpChild)
                if depht > 2 :
                    dpChild[u"children"] = []
                    # Depht 3 - ROMEFi
                    fiList = getFieldChoicesROME__byLetter(ROMEFi,dp[0][0:3])
                    for fi in fiList:
                        fiChild = {}
                        fiChild[u"name"] = fi[0]
                        dpChild[u"children"].append(fiChild)
                        if depht > 3 :
                            fiChild[u"children"] = []
                            # Depht 3 - ROMEFi
                            apList = getFieldChoicesROME__byLetter(ROMEAp,fi[0][0:5])
                            for ap in apList:
                                apChild = {}
                                apChild[u"name"] = ap[0]
                                fiChild[u"children"].append(apChild)
                                # Last level of depht : always do this
                                apChild[u"size"] = 10000
                                # Last level of depht : never do this
                                #apChild[u"children"] = []
                        else:
                            fiChild[u"size"] = 10000
                else:
                    dpChild[u"size"] = 10000
        else:
            gdChild[u"size"] = 10000
    return json.dumps(rootObject)

def connectROMEModels(level=111):
    iLevel = level - 100
    if iLevel >= 0:
        #niveau 1 : DP liés aux GD
        cnt = 0
        for o in ROMEDP.objects.all():
            o.parent = o.connect()
            o.save()
            cnt += 1
        print u"[ACTIVELIFE] Domaines professionnels ROME reliés à leur grand domaine : " + u"%i" % cnt
    else:
        iLevel = level
    iLevel = level - 10
    if iLevel >= 0:
        #niveau 2 : Fi liées aux DP
        cnt = 0
        for o in ROMEFi.objects.all():
            o.parent = o.connect()
            o.save()
            cnt += 1
        print u"[ACTIVELIFE] Fiches ROME reliées à leur domaine professionnel : " + u"%i" % cnt
    else:
        iLevel = level
    iLevel = level - 1
    if iLevel >= 0:
        #niveau 3 : Ap liées aux Fi
        cnt = 0
        for o in ROMEAp.objects.all():
            o.parent = o.connect()
            o.save()
            cnt += 1
        print u"[ACTIVELIFE] Appellations OGR reliées à leur fiche ROME : " + u"%i" % cnt
    else:
        iLevel = level

def deleteROMEModels(level=1111):
    iLevel = level - 1000
    if iLevel >= 0:
        #niveau 1 : GD
        print u"[ACTIVELIFE] Grands domaines ROME présents avant suppression : " + u"%i" % len(ROMEGD.objects.all())
        ROMEGD.objects.all().delete()
        print u"[ACTIVELIFE] Grands domaines ROME présents après suppression : " + u"%i" % len(ROMEGD.objects.all())
    else:
        iLevel = level
    iLevel = level - 100
    if iLevel >= 0:
        #niveau 2 : DP
        print u"[ACTIVELIFE] Domaines professionnels ROME présents avant suppression : " + u"%i" % len(ROMEDP.objects.all())
        ROMEDP.objects.all().delete()
        print u"[ACTIVELIFE] Domaines professionnels ROME présents après suppression : " + u"%i" % len(ROMEDP.objects.all())
    else:
        iLevel = level
    iLevel = level - 10
    if iLevel >= 0:
        #niveau 3 : Fi
        print u"[ACTIVELIFE] Fiches ROME présentes avant suppression : " + u"%i" % len(ROMEFi.objects.all())
        ROMEFi.objects.all().delete()
        print u"[ACTIVELIFE] Fiches ROME présentes après suppression : " + u"%i" % len(ROMEFi.objects.all())
    else:
        iLevel = level
    iLevel = level - 1
    if iLevel >= 0:
        #niveau 4 : Ap
        print u"[ACTIVELIFE] Appellations OGR présentes avant suppression : " + u"%i" % len(ROMEAp.objects.all())
        ROMEAp.objects.all().delete()
        print u"[ACTIVELIFE] Appellations OGR présentes après suppression : " + u"%i" % len(ROMEAp.objects.all())
    else:
        iLevel = level

def loadROMEModels(level=1111):
    deleteROMEModels(level)
    iLevel = level - 1000
    if iLevel >= 0:
        #niveau 1 : GD
        print u"[ACTIVELIFE] Grands domaines ROME déjà présents : " + u"%i" % len(ROMEGD.objects.all())
        cnt = 0
        data = PE_access_dataset(u"ROME_GRAND_DOMAINE")
        for r in data[u'result'][u'records']:
            gd = ROMEGD(code=r[u'MAIN_PROF_AREA_CODE'],text=r[u'MAIN_PROF_AREA_NAME'])
            gd.save()
            fieldChoicesROME__[ROMEGD].append((gd.__unicode__(),gd.__unicode__()))
            cnt += 1
        print u"[ACTIVELIFE] Grands domaines ROME enregistrés : " + u"%i" % cnt
        print u"[ACTIVELIFE] Grands domaines ROME désormais présents : " + u"%i" % len(ROMEGD.objects.all())
    else:
        iLevel = level
    iLevel = level - 100
    if iLevel >= 0:
        #niveau 2 : DP
        print u"[ACTIVELIFE] Domaines professionels ROME déjà présents : " + u"%i" % len(ROMEDP.objects.all())
        cnt = 0
        data = PE_access_dataset(u"ROME_DOMAINE_PRO")
        for r in data[u'result'][u'records']:
            dp = ROMEDP(code=r[u'PROFESSIONAL_AREA_CODE'],text=r[u'PROFESSIONAL_AREA_NAME'])
            dp.save()
            fieldChoicesROME__[ROMEDP].append((dp.__unicode__(),dp.__unicode__()))
            cnt += 1
        print u"[ACTIVELIFE] Domaines professionels ROME enregistrés : " + u"%i" % cnt
        print u"[ACTIVELIFE] Domaines professionels ROME désormais présents : " + u"%i" % len(ROMEDP.objects.all())
        connectROMEModels(100)
        print u"[ACTIVELIFE] Domaines professionels ROME connectés à leurs parents."
    else:
        iLevel = level
    iLevel = level - 10
    if iLevel >= 0:
        #niveau 3 : Fi
        print u"[ACTIVELIFE] Fiches ROME déjà présentes : " + u"%i" % len(ROMEFi.objects.all())
        cnt = 0
        data = PE_access_dataset(u"REF_CODE_ROME")
        for r in data[u'result'][u'records']:
            fi = ROMEFi(code=r[u'ROME_PROFESSION_CARD_CODE'],text=r[u'ROME_PROFESSION_CARD_NAME'])
            fi.save()
            fieldChoicesROME__[ROMEFi].append((fi.__unicode__(),fi.__unicode__()))
            cnt += 1
        print u"[ACTIVELIFE] Fiches ROME enregistrées : " + u"%i" % cnt
        print u"[ACTIVELIFE] Fiches ROME désormais présentes : " + u"%i" % len(ROMEFi.objects.all())
        connectROMEModels(10)
        print u"[ACTIVELIFE] Fiches ROME connectées à leurs parents."
    else:
        iLevel = level
    iLevel = level - 1
    if iLevel >= 0:
        #niveau 4 : Ap
        print u"[ACTIVELIFE] Appellations ROME déjà présentes : " + u"%i" % len(ROMEAp.objects.all())
        iLimit = 1000
        cnt = 0
        iTotal = iLimit
        while cnt < iTotal:
            data = PE_access_dataset(u"REF_APPELLATION",limit=iLimit,offset=cnt)
            iTotal = data[u'result'][u'total']
            for r in data[u'result'][u'records']:
                ap = ROMEAp(codeOGR=r[u'\ufeffOGR_CODE'],codeROME=r[u'ROME_PROFESSION_CARD_CODE'],text=r[u'ROME_PROFESSION_NAME'])
                ap.save()
                fieldChoicesROME__[ROMEAp].append((ap.__unicode__(),ap.__unicode__()))
                cnt += 1
        print u"[ACTIVELIFE] Appellations ROME enregistrées : " + u"%i" % cnt
        print u"[ACTIVELIFE] Appellations ROME désormais présentes : " + u"%i" % len(ROMEAp.objects.all())
        connectROMEModels(1)
        print u"[ACTIVELIFE] Appellations ROME connectées à leurs parents."
    else:
        iLevel = level

class ACTIVLTiers(models.Model):
    nom = models.CharField(max_length=100,default='')
    prenom = models.CharField(max_length=100,default='')
    genre = models.CharField(max_length=100, choices = ( (u"Femme",u"Femme"), (u"Homme",u"Homme"), (u"Non renseigné",u"Non renseigné") ) ,default='')
    anniversaire = models.DateTimeField('Date de naissance',default='',null=True)
    typetiers = models.CharField(max_length=100, choices = ( (u"Candidat",u"Candidat"), (u"Recruteur",u"Recruteur") ) ,editable=False,null=True)
    def __unicode__(self):
        return self.prenom + u" " + self.nom

class ACTIVLCandidat(models.Model):
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
    identPE = models.CharField(max_length=16,default='')
    def __unicode__(self):
        return u"Candidat " + self.identPE + u" ( " + self.tiers.__unicode__() + u" )"

class ACTIVLRecruteur(models.Model):
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
    raisonSociale = models.CharField(max_length=200)
    SIRET = models.CharField(max_length=14)
    def __unicode__(self):
        return u"Recruteur " + self.raisonSociale + u" SIRET " + self.SIRET + u" ( " + self.tiers.__unicode__() + u" )"

class ACTIVLCritMetierROMEGD(models.Model):
    valeur = models.CharField(max_length=100, choices = getFieldChoicesROME__(ROMEGD) )
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritMetierROMEDP(models.Model):
    valeur = models.CharField(max_length=100, choices = getFieldChoicesROME__(ROMEDP) )
    parent = models.ForeignKey(ACTIVLCritMetierROMEGD,on_delete=models.CASCADE,null=True)
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritMetierROMEFi(models.Model):
    valeur = models.CharField(max_length=100, choices = getFieldChoicesROME__(ROMEFi) )
    parent = models.ForeignKey(ACTIVLCritMetierROMEDP,on_delete=models.CASCADE,null=True)
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritMetierROMEAp(models.Model):
    valeur = models.CharField(max_length=100, choices = getFieldChoicesROME__(ROMEAp) )
    parent = models.ForeignKey(ACTIVLCritMetierROMEFi,on_delete=models.CASCADE,null=True)
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)

class ACTIVLCritExperience(models.Model):
    valeur = models.IntegerField(null=True)
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritSalaireJour(models.Model):
    valeur = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritSalaireMois(models.Model):
    valeur = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritSalaireAn(models.Model):
    valeur = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritVille(models.Model):
    valeur = models.CharField(max_length=100, null=True )
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
class ACTIVLCritRegion(models.Model):
    valeur = models.CharField(max_length=100, null=True )
    tiers = models.ForeignKey(ACTIVLTiers,on_delete=models.CASCADE,null=True)
