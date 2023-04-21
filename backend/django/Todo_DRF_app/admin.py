from django.contrib import admin
from .models import CustomUser,Project,TaskList,Task

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(TaskList)
admin.site.register(Task)