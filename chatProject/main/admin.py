from django.contrib import admin
from .models import Profile, Messages, UserLogs

# Register your models here.
admin.site.register(Profile)
admin.site.register(Messages)
admin.site.register(UserLogs)
