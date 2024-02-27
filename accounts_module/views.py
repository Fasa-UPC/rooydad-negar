from django.contrib.auth import login
from django.shortcuts import render
from django.views import View
from .forms import *
from events_module.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

class RegisterUser(View):
    def get(self, request):
        form = RegisterForm()
        fields = Field.objects.all()
        return render(request, 'register.html', context={
            'from': form,
            'fields': fields
        })

    def post(self, request):
        form = RegisterForm(data=request.POST)
        fields = Field.objects.all()
        if form.is_valid():
            user = User()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.username = form.cleaned_data.get('phone_number')
            user.student_code = form.cleaned_data.get('student_code')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.entering_year = form.cleaned_data.get('entering_year')
            user.field_of_study = form.cleaned_data.get('field_of_study')
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return render(request, 'register.html', context={
                'from': form,
                'fields': fields
            })
        else:
            return render(request, 'register.html', context={
                'form': form,
                'fields': fields
            })


class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', context={
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
            return render(request, 'profile.html', context={'user': user})
        else:
            return render(request, 'login.html', {'form': form})


@login_required(login_url='/account/login')
def profile(request):
    user = request.user
    user_events = Participant.objects.filter(user=user, status=True).all()
    return render(request, 'profile.html', {
        'user': user,
        'events': user_events
    })
