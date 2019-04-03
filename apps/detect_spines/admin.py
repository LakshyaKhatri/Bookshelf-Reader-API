from django.contrib import admin
from .models import Bookshelf, Spine

# Register your models here.
admin.site.register(Bookshelf)
admin.site.register(Spine)
