from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Discount)
admin.site.register(UserDescount)