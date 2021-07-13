from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from common.utils import handle_uploaded_file


def index(request):
    """
    Homepage view. Show question list for authenticated user.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("qa:index"))
    else:
        return render(request, "web/index.html")


@method_decorator(login_required, name="dispatch")
class TrixUploadFile(View):
    """
    This view handle ajax post request for uploading image files from trix editor.
    Javascript codes to call this view located in web/static/js/trixUpload.js
    """

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data["file"], form.cleaned_data["key"])
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"status": 500, "errors": form.errors})
