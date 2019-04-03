from rest_framework import generics
from detect_spines.models import Bookshelf
from .serializers import BookshelfSerializer


class CreateBookshelfView(generics.CreateAPIView):
    queryset = Bookshelf.objects.all()
    serializer_class = BookshelfSerializer
