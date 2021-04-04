from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'qa/index.html')
    else:
        return render(request, 'web/index.html')
