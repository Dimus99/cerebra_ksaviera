from django.shortcuts import render

from api.controller import get_mix_open_requests, get_mix_projects


def index(request):
    if "text" in request.POST:
        limit = request.POST.get("limit") or 5
        limit = int(limit)
        res = get_mix_projects(request.POST["text"], limit)
        return render(request, "index.html", context={"variants": res, "text": request.POST["text"]})
    return render(request, "index.html")


def task2(request):
    if "text" in request.POST:
        limit = request.POST.get("limit") or 5
        limit = int(limit)
        res = get_mix_open_requests(request.POST["text"], limit)
        return render(request, "task2.html", context={"variants": res, "text": request.POST["text"]})
    return render(request, "task2.html")
