from django.db import models
import os
import spine_detection
from django.core.files.base import File
import scrap_book
import random
# Create your models here.


def bookshelf_image_path(instance, filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    new_filename = 'bookshelf'
    new_filename = "{new_filename}{ext}".format(
        new_filename=new_filename,
        ext=ext
    )

    return "bookshelfs/{new_filename}".format(
        new_filename=new_filename
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
            processed_image, extension = spine_detection.draw_spine_lines(self.image)
            self.spine_line_drawn_image.save(
                "image.{extension}".format(extension=extension.lower()),
                File(processed_image),
                save=False
            )
            super(Bookshelf, self).save(*args, **kwargs)

            # Creates and saves cropped spines to database
            spine_images = spine_detection.get_spines(self.image)

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


class Book(models.Model):
    title = models.CharField(max_length=500, null=False)
    author = models.CharField(max_length=500, null=True, blank=True)
    price = models.CharField(max_length=20, null=True, blank=True)
    rating = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    publisher = models.CharField(max_length=500, null=True, blank=True)
    isbn_10 = models.CharField(max_length=20, null=True, blank=True)
    isbn_13 = models.CharField(max_length=20, null=True, blank=True)
    total_pages = models.CharField(max_length=10, null=True, blank=True)
    genre = models.CharField(max_length=500, null=True, blank=True)
    dimensions = models.CharField(max_length=500, null=True, blank=True)
    book_cover_url = models.CharField(max_length=32656232365, null=True, blank=True)

    def __str__(self):
        return "{id}. {book_title}".format(id=self.id, book_title=self.title)

    def save(self, *args, **kwargs):
        # fetch book cover image URL and isbn then save the object
        if self.id is None:
            self.title = str(self.title).title()
            bookInfo = scrap_book.get_book_info(self.title)
            self.title = bookInfo.title
            self.author = bookInfo.author
            # TODO: Add actual price
            self.price = "Rs. " + str(random.randint(100, 500)) + ".00"
            self.rating = bookInfo.rating
            self.description = bookInfo.description
            self.publisher = bookInfo.publisher
            self.isbn_10 = bookInfo.isbn_10
            self.isbn_13 = bookInfo.isbn_13
            self.total_pages = bookInfo.total_pages
            self.genre = bookInfo.genre
            # TODO: Add actual dimensions
            self.dimensions = "19.7 x 13 x 2.2 cm"
            self.book_cover_url = bookInfo.image_url
            super(Book, self).save(*args, **kwargs)
