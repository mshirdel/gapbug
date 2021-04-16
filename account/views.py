from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from user_profile.models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            profile.send_verification_email(request)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def profile(request, id):
    user = get_object_or_404(User, pk=id)
    return render(request, 'account/profile.html',
                  {
                      'user_profile': user
                  })
