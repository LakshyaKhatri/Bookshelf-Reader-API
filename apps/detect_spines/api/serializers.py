from rest_framework import serializers
from detect_spines.models import Bookshelf


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = "__all__"
