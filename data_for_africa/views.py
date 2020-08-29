from django.http import JsonResponse


def ping(request):
    data = {"ping": "pongss!"}
    return JsonResponse(data)
