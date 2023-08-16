from django.contrib import admin

# Register your models here.
from .models import command_db,current_db,main_db

admin.site.register(command_db)
admin.site.register(current_db)
admin.site.register(main_db)
