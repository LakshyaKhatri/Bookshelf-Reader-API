from rest_framework import serializers
from detect_spines.models import Bookshelf, Spine, Book


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = "__all__"


class SpineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spine
        fields = ("image", )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
