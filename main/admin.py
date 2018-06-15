from django.contrib import admin
from .models import Developer, Agent, Property, Mortage
# Register your models here.
admin.site.register(Property)
admin.site.register(Developer)
admin.site.register(Agent)
admin.site.register(Mortage)