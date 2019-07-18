from django.shortcuts import render, redirect
from .forms import UserRegsiterForm, ProfileRegsiterForm
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegsiterForm(data = request.POST)
        profile_form = ProfileRegsiterForm(data = request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()

            return redirect('home')
        
    else :
        user_form = UserRegsiterForm(instance=request.user)
        profile_form = ProfileRegsiterForm(instance=request.user.profile)
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })