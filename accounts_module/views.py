from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from events_module.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

class RegisterUser(View):
    def get(self, request):
        form = RegisterForm()
        fields = Field.objects.all()
        return render(request, 'module/register.html', context={
            'form': form,
            'fields': fields
        })

    def post(self, request):
        form = RegisterForm(data=request.POST)
        fields = Field.objects.all()
        if form.is_valid():
            user = User(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                username=form.cleaned_data.get('phone_number'),
                student_code=form.cleaned_data.get('student_code'),
                phone_number=form.cleaned_data.get('phone_number'),
                entering_year=form.cleaned_data.get('entering_year'),
                field_of_study=form.cleaned_data.get('field_of_study')
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return render(request, 'module/register.html', context={
                'form': form,
                'fields': fields,
                'is_successful': True,
            })
        else:
            return render(request, 'module/register.html', context={
                'form': form,
                'fields': fields,
                'is_successful': False,
            })


class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'module/login.html', context={
            'form': form
        })

    def post(self, request):
        form = LoginForm(data=request.POST)
        user = None
        if form.is_valid():
            user = User.objects.filter(phone_number__iexact=form.cleaned_data.get('phone_number')).first()
            if user is not None:
                is_valid_password = user.check_password(form.cleaned_data.get('password'))
                if is_valid_password:
                    login(request, user)
                else:
                    form.add_error('password', "کلمه عبور نادرست")
            else:
                form.add_error('phone_number', "کاربر یافت نشد")

        if user is not None:
            return render(request, 'module/profile.html', context={'user': user})
        else:
            return render(request, 'module/login.html', {'form': form})


@login_required(login_url='/account/login')
def profile(request):
    user = request.user
    user_events = Participant.objects.filter(user=user, status=True).all()
    return render(request, 'module/profile.html', {
        'user': user,
        'events': user_events
    })

@login_required(login_url='/account/login')
def profile_events(request):
    user = request.user
    user_events = Participant.objects.filter(user=user, status=True).all()
    return render(request, 'module/profile_events.html', {
        'user': user,
        'events': user_events
    })

def logout_user(request):
    logout(request)
    return redirect("events:events")