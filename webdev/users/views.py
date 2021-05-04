from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('produtos:estoque_produtos')
    else:
        form = AuthenticationForm()

    context = {
        'title': 'Boas-vindas!',
        'form': form
    }

    return render(request, 'users/login.html', context)