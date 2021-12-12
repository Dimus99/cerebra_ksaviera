from django.http import HttpResponse
from api.controller import get_mix_open_requests, get_mix_projects


def index(request):
    return HttpResponse("Hi")


def mix_variants(request):
    arg = request.POST.get("text")
    limit = request.POST.get("limit") or 5
    result = get_mix_projects(arg, limit)
    return HttpResponse(str(result))  # need serialize


def mix_open_requests(request):
    arg = request.POST.get("text")
    limit = request.POST.get("limit") or 5
    result = get_mix_open_requests(arg, limit)
    return HttpResponse(str(result))  # need serialize
