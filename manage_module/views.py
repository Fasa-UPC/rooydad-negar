from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from accounts_module.models import User, Field
from events_module.models import Event, Participant, Discount
from functions.process import save_to_csv


# Create your views here.
class ManageUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                users = User.objects.all()
                fields = Field.objects.all()
                return render(request, 'module/users.html', {'users': users, 'fields': fields})
        return HttpResponse("ظاهرا گم شدید")


class UserDetail(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                user = User.objects.get(id=pk)
                events = Participant.objects.filter(user_id=pk)
                return render(request, 'module/user.html', {'user': user, 'events': events})
        return HttpResponse("ظاهرا گم شدید")


class ManageEvents(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                events = Event.objects.all()
                return render(request, 'module/manage_events.html', {'events': events})
        return HttpResponse("ظاهرا گم شدید")


class ShowEventsInfo(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                event = Event.objects.get(id=pk)
                users = Participant.objects.filter(event_id=pk).all()
                amount = 0
                for user in users:
                    if user.total > 0:
                        amount += user.total
                    else:
                        ...

                return render(request, 'module/show_event_info.html', context={
                    'event': event,
                    'users': users,
                    'count': users.count(),
                    'amount': amount
                })
        return HttpResponse("ظاهرا گم شدید")


def download_event_state(request, pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            event = Event.objects.get(id=pk)
            users = Participant.objects.filter(event_id=pk).all()
            filename = f"{event.title}.csv"
            file_path = save_to_csv(users, filename)

            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
    return HttpResponse("ظاهرا گم شدید")


def user_info_by_field(request, pk):
    users = User.objects.filter(field_of_study__slug=pk).all()
    print(users)
    fields = Field.objects.all()
    return render(request, 'module/users.html', {
        'users': users,
        'fields': fields
    })

def cancel_event(request, event, user):
    founder = Participant.objects.filter(event_id=event, user_id=user)
    if founder:
        founder.delete()
    else:
        HttpResponse("Error")
    return redirect('manage:events')

def manage_discount(request):
    codes = Discount.objects.all()
    return render(request,'module/discount.html', context={'code': codes})