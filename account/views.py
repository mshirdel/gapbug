from django.shortcuts import render
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
            # TODO: Email verification:
            # 1- create profile
            Profile.objects.create(user=new_user)
            # 2- generate email verification token
            # 3- send mail
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def profile(request):
    return render(request, 'account/profile.html')
