from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RegistrationForm
from django.views.generic.edit import View


class RegistrationView(View):

    def get(self, request):
        user_form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': user_form})

    def post(self, request):
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user = authenticate(
                username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, 'registration/register.html', {'form': user_form})
