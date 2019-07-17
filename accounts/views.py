from django.shortcuts import render, redirect
from .forms import UserRegsiterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegsiterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('home')
    else :
        form = UserRegsiterForm()
    return render(request, 'accounts/register.html', {'form' : form})