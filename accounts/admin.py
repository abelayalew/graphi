from django.contrib import admin
from django.contrib.auth.models import Permission

from accounts.models import OTP, User, Employee

admin.site.register(Permission)
admin.site.register(User)
admin.site.register(OTP)
admin.site.register(Employee)
