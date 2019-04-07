from django.contrib import admin
from .models import Bookshelf, Spine, Book

# Register your models here.
admin.site.register(Bookshelf)
admin.site.register(Spine)
admin.site.register(Book)
