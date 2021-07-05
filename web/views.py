from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
import logging


logger = logging.getLogger(__name__)


def index(request):
    logger.info('index ok ok ok')
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('qa:index'))
    else:
        return render(request, 'web/index.html')
