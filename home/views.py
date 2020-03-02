from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import translation
from datetime import date
from django.utils import formats
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language
from clinic.models import Clinic
from .forms import AddUserForm

def viewAR(request):
    user_language = 'ar'
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def viewEN(request):
    user_language = 'en-us'
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def user_login(request):
    next = request.GET.get('next')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if next:
                    return redirect(next)
                return HttpResponseRedirect(reverse('home:homepage'))
            else:
                messages.error(request, 'Inactive Account')
                return render(request, 'login.html')
        else:
            messages.error(request, _(
                'Login Failed, Please Check the Username or Password'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required(login_url='/login')
def homepage(request):
    return render(request, 'index.html', context=None)


@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:user-login'))


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            clinic = Clinic(
                           clinic_name = form.cleaned_data.get('clinic_form_name'),
                           )
            clinic.save()
            user.clinic_id = clinic.id
            user.save(update_fields=['clinic'])
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home:homepage'))
            else:
                user_lang=user_lang=to_locale(get_language())
                if user_lang=='ar':
                    messages.error(request, 'This account is deactivated!')
                else:
                    messages.error(request, 'This Account is inactive!')
                return render(request, 'login.html')
    return render(request, 'register.html', {'register_form': form})

def addUserView(request):
    form = AddUserForm()
    print(request.user.email)
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.clinic = request.user.clinic
            user.save()
            user_lang=to_locale(get_language())
            if user_lang=='ar':
                success_msg = 'تم الانشاء بنجاح'
            else:
                success_msg ='Create Successfully'

            messages.success(request, success_msg)
        else:  # Form was not valid
            # success_msg = 'The form is not valid.'
            user_lang=to_locale(get_language())
            if user_lang=='ar':
                success_msg = 'لم يتم الانشاء بنجاح'
            else:
                success_msg ='The form is not valid.'
            messages.error(request, form.errors)
    myContext = {
                 'page_title':"Create New User",
                 'add_user': form,
    }
    return render(request, 'add-user.html', myContext)
