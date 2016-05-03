from django.http import HttpResponse

def racine(request):
    return HttpResponse("Projet Django de JV")
