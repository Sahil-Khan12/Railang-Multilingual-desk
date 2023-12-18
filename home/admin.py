from django.contrib import admin
from .models import Train,Logic1
# Register your models here.
class Search(admin.ModelAdmin):
    search_fields=('Train_No',)

admin.site.register(Train,Search)
admin.site.register(Logic1)
