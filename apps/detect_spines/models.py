from django.db import models
import os
# Create your models here.


def upload_image_path(instance, filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    print(name, ext)
    new_filename = 'image'
    final_filname = "{new_filename}{ext}".format(
        new_filename=new_filename,
        ext=ext
    )

    return "books_unseprated/{final_filname}".format(
        final_filname=final_filname
    )


class Book(models.Model):
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.id


class Spine(models.Model):
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
