# -*- coding: cp1252 -*-
import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.

from .models import *

def testeUniciteChampModele(ModelClass, attrName):
    if attrName in ModelClass._meta._forward_fields_map:
        testVals = {}
        for o in ModelClass.objects.all():
            val = o.__dict__[attrName]
            if val in testVals:
                testVals[val] += 1
                return False
            else:
                testVals[val] = 1
        return True
    else:
        return False

class ROMETestsUniciteTexte(TestCase):
    def test_ROMEGDUniciteTexte(self):
        self.assertEqual(testeUniciteChampModele(ROMEGD, 'text'), True)
    def test_ROMEDPUniciteTexte(self):
        self.assertEqual(testeUniciteChampModele(ROMEDP, 'text'), True)
    def test_ROMEFiUniciteTexte(self):
        self.assertEqual(testeUniciteChampModele(ROMEFi, 'text'), True)
    def test_ROMEApUniciteTexte(self):
        self.assertEqual(testeUniciteChampModele(ROMEAp, 'text'), True)
class ROMETestsUniciteCode(TestCase):
    def test_ROMEGDUniciteCode(self):
        self.assertEqual(testeUniciteChampModele(ROMEGD, 'code'), True)
    def test_ROMEDPUniciteCode(self):
        self.assertEqual(testeUniciteChampModele(ROMEDP, 'code'), True)
    def test_ROMEFiUniciteCode(self):
        self.assertEqual(testeUniciteChampModele(ROMEFi, 'code'), True)
    def test_ROMEApUniciteCode(self):
        self.assertEqual(testeUniciteChampModele(ROMEAp, 'codeOGR'), True)
