from django.http import JsonResponse


def ping(request):
    data = {"ping": "team 1.0.1, let's get our hands dirty!"}
    return JsonResponse(data)
