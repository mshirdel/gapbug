from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qa:index'))
    else:
        return render(request, 'web/index.html')
