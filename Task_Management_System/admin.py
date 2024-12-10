from django.contrib import admin
from .models import User,Task,Comment


 
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(User)

 
