from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import *
from django.contrib import messages
from functions.main import percent_maker
from django.contrib.auth.decorators import login_required


# Create your views here.
class EventsList(ListView):
    queryset = Event.objects.filter(status=True).all()
    context_object_name = 'events'
    template_name = 'module/events.html'


def event_detail(request, pk):
    event = get_object_or_404(Event, slug=pk)
    if request.user.is_authenticated:
        is_registered = Participant.objects.filter(user=request.user, status=True).values_list('event_id', flat=True)
    else:
        is_registered = False
    return render(request, 'module/details.html', context={
        'event': event,
        'is_registered': is_registered
    })


@login_required(login_url="/account/login")
def register_event(request, pk):
    event = Event.objects.get(id=pk)
    current_event = Participant.objects.filter(status=False, user=request.user)
    current_event.delete()
    UserDescount.objects.filter(user=request.user, status=False).delete()
    if event.status == True:
        if event.capacity >= 1:
            new_registration = Participant(user=request.user, event=event,
                                           total=Event.objects.get(id=pk).price)
            new_registration.save()
            return redirect('events:card')
        else:
            return HttpResponse("ظرفیت ثبت نام دوره به پایان رسیده است")
    else:
        return HttpResponse("ثبت نام این دوره غیرفعال است")


@login_required(login_url="/account/login")
def card(request):
    user_card: Participant = Participant.objects.filter(status=False, user=request.user).first()
    user = request.user
    if request.method == 'POST':
        code = request.POST.get('discount')
        exists_code: Discount = Discount.objects.filter(code=code).first()
        useable = UserDescount.objects.filter(user=request.user, code=code).exists()
        if exists_code and exists_code.status == True and exists_code.count >= 1:
            if not useable:

                UserDescount.objects.get_or_create(user=request.user, code=code)
                user_card.total = percent_maker(user_card.total, exists_code.percent)
                user_card.save()
                messages.success(request, "کد تخفیف اعمال شد")
            else:
                messages.error(request, "این کد را قبلا استفاده کرده اید")
        else:
            messages.error(request, "کد تخفیف وجود ندارد یا ظرفیت آن به پایان رسیده")
    return render(request, 'module/card.html', context={
        'user_card': user_card,
        'user': user
    })
