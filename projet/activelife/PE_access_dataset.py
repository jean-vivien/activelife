# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 01:38:41 2016

@author: jean-vivien
"""

import pycurl
import certifi
import json
from StringIO import StringIO
import pprint
import time

import codecs

ESD_client_id = 'ESD_chomage-jv_b871cb028b47e423019d52d92470548f1034d82fcdae54bfa62c53f1d85b8c32'
ESD_secret_key = 'a27c52ac9e9d2d87063460d116db484e781bf10b18bb0b2c408e958c67f53a8b'

def PE_access_dataset(pe_source,limit=100000,offset=0):

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.emploi-store-dev.fr/identite/oauth2/access_token?realm=developpeur&grant_type=client_credentials&client_id=' + ESD_client_id + '&client_secret=' + ESD_secret_key)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.VERBOSE, True)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(pycurl.POST, 1)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    #print "========== Response body ============"
    #print(body)

    ESD_token = json.loads(body)

    #print "========== Parsed token ============"
    #print(ESD_token["access_token"])

    buffer2 = StringIO() # apparemment il vaut mieux recréer un nouvel objet ici
    c2 = pycurl.Curl()
    #on doit mettre non seulement le host mais également l'URL complète dans ce paramètre
    c2.setopt(c2.URL, 'https://api.emploi-store.fr/api/action/organization_show?id=digidata')
    c2.setopt(c2.WRITEDATA, buffer2)
    c2.setopt(c2.VERBOSE, True)
    c2.setopt(c2.FOLLOWLOCATION, True)
    c2.setopt(c2.CAINFO, certifi.where())
    c2.setopt(c2.HTTPGET, 1)
    headers = [
        "GET /api/action/organization_show?id=digidata HTTP/1.1",
        "Host: api.emploi-store.fr",
        "Authorization: Bearer "+ESD_token["access_token"]
                ]
    c2.setopt(c2.HTTPHEADER, headers)
    c2.perform()
    body = buffer2.getvalue()
    #print "========== Response body (2) ============"
    #print(body)
    c2.close()

    ESD_organizations = json.loads(body)
    pp = pprint.PrettyPrinter(indent=4,depth=10)
    #print "========== JSON Pretty print ES package list ============"
    #pp.pprint(ESD_organizations)

    id_rome = u'Pas trouvée'
    package_list = ESD_organizations[u'result'][u'packages']
    for p in package_list:
        if p[u'name'] == u'rome':
            id_rome = p[u'id']
            print "========== id of package u'rome' ============"
            print id_rome
    #    print "========== ES package list, name/id ============"
    #    print p[u'name']
    #    print p[u'id']
            break

    #if("result" in ESD_organizations):
    #    if "organization" in ESD_organizations["result"]:
    #        print()


    buffer3 = StringIO() # apparemment il vaut mieux recréer un nouvel objet ici
    c3 = pycurl.Curl()
    #on doit mettre non seulement le host mais également l'URL complète dans ce paramètre
    c3.setopt(c3.URL, 'https://api.emploi-store.fr/api/action/package_show?id='+id_rome)
    c3.setopt(c3.WRITEDATA, buffer3)
    c3.setopt(c3.VERBOSE, True)
    c3.setopt(c3.FOLLOWLOCATION, True)
    c3.setopt(c3.CAINFO, certifi.where())
    c3.setopt(c3.HTTPGET, 1)
    headers = [
        "GET /api/action/package_show?id="+id_rome+" HTTP/1.1",
        "Host: api.emploi-store.fr",
        "Authorization: Bearer "+ESD_token["access_token"]
                ]
    c3.setopt(c3.HTTPHEADER, headers)
    c3.perform()
    body = buffer3.getvalue()
    print "========== Response body (3) ============"
    print(body)
    c3.close()

    ESD_package_rome = json.loads(body)
    print "========== JSON Pretty print ES package rome ============"
    pp.pprint(ESD_package_rome)
    filename = "body_3_" + time.strftime("%y%m%d%H%M%S")
    with open(filename, 'wb') as f:
        f.write(body)
    ROME_TYPE_REF_id = ""
    ROME_TYPE_REF_url = ""
    filenameRefs = "refsPE_" + time.strftime("%y%m%d%H%M%S")
    fRefs=codecs.open(filenameRefs, 'wb', encoding='utf-8')
    fRefs.write(u"pe_source,description,url\n")
    fRefs.close()
    for r in ESD_package_rome[u"result"][u"resources"]:
        lineRefs = r[u"pe_source"]+u","+r[u"description"]+u","+r[u"url"]+u"\n"
        fRefs=codecs.open(filenameRefs, 'ab', encoding='utf-8')
        fRefs.write(lineRefs)
        fRefs.close()
        #if r[u"pe_source"] == u"ROME_TYPE_REF":
        if r[u"pe_source"] == pe_source:
            ROME_TYPE_REF_id = r[u"id"]
            ROME_TYPE_REF_url = r[u"url"]
            print "========== id of resource ROME_TYPE_REF ============"
            print ROME_TYPE_REF_id
            print "========== url of resource ROME_TYPE_REF ============"
            print ROME_TYPE_REF_url

    buffer4 = StringIO() # apparemment il vaut mieux recréer un nouvel objet ici
    c4 = pycurl.Curl()
    #on doit mettre non seulement le host mais également l'URL complète dans ce paramètre
    c4.setopt(pycurl.URL, 'https://api.emploi-store.fr/api/action/datastore_search?resource_id='+ROME_TYPE_REF_id+'&limit='+u'%i' % limit + "&offset="+u"%i" % offset)
    c4.setopt(pycurl.WRITEDATA, buffer4)
    c4.setopt(pycurl.VERBOSE, True)
    c4.setopt(pycurl.FOLLOWLOCATION, True)
    c4.setopt(pycurl.CAINFO, certifi.where())
    c4.setopt(pycurl.HTTPGET, 1)
    headers = [
        "GET /api/action/datastore_search?resource_id="+ROME_TYPE_REF_id+"&limit="+u"%i" % limit + "&offset="+u"%i" % offset + u" HTTP/1.1",
        "Host: api.emploi-store.fr",
        "Authorization: Bearer "+ESD_token["access_token"]
                ]
    c4.setopt(pycurl.HTTPHEADER, headers)
    c4.perform()
    body = buffer4.getvalue()
    filename = "body_4_" + time.strftime("%y%m%d%H%M%S")
    with open(filename, 'wb') as f:
        f.write(body)
    print "========== Response body (4) ============"
    print(body)
    c4.close()

    return json.loads(body)
