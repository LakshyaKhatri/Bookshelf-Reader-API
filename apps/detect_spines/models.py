from django.db import models
import os
import spine_detection
from django.core.files.base import File
# Create your models here.


def bookshelf_image_path(instance, filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    new_filename = 'bookshelf'
    final_filname = "{new_filename}{ext}".format(
        new_filename=new_filename,
        ext=ext
    )

    return "bookshelfs/{final_filname}".format(
        final_filname=final_filname
    )


def spine_drawn_bookshelf_image_path(instance, filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    new_filename = 'spine-drawn-bookshelf'
    final_filname = "{new_filename}{ext}".format(
        new_filename=new_filename,
        ext=ext
    )

    return "spine-drawn-bookshelfs/{final_filname}".format(
        final_filname=final_filname
    )


def spine_image_path(instance, filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    new_filename = 'spine'
    final_filname = "{new_filename}{ext}".format(
        new_filename=new_filename,
        ext=ext
    )

    return "spines/{final_filname}".format(final_filname=final_filname)


class Bookshelf(models.Model):
    image = models.ImageField(upload_to=bookshelf_image_path)
    spine_line_drawn_image = models.ImageField(
        upload_to=spine_drawn_bookshelf_image_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Saves an image with spine lines drawn on it.
        if self.id is None:
            processed_image, extension = spine_detection.drawSpineLines(self.image)
            self.spine_line_drawn_image.save(
                "image.{extension}".format(extension=extension.lower()),
                File(processed_image),
                save=False
            )
            super(Bookshelf, self).save(*args, **kwargs)

            # Creates and saves cropped spines to database
            spine_images = spine_detection.getSpines(self.image)

            for spine_image in spine_images:
                spine = Spine.objects.create(bookshelf=self)
                spine.image.save(
                    "image.{extension}".format(extension=extension.lower()),
                    File(spine_image),
                    save=True
                )

    def __str__(self):
        return str(self.id)


class Spine(models.Model):
    image = models.ImageField(upload_to=spine_image_path, null=True, blank=True)
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)

    def __str__(self):
        return "{book_id} : {spine_number}".format(
            book_id=self.bookshelf.id,
            spine_number=self.id
        )
