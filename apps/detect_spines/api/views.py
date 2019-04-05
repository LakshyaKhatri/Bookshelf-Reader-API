from rest_framework import generics
from detect_spines.models import Bookshelf, Spine
from .serializers import BookshelfSerializer, SpineListSerializer
from rest_framework import status
from rest_framework.response import Response


class CreateBookshelfView(generics.CreateAPIView):
    queryset = Bookshelf.objects.all()
    serializer_class = BookshelfSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        headers['id'] = obj.id
        response = Response({"Success": "Created Successfully"},
                            status=status.HTTP_201_CREATED, headers=headers)
        return response


class GetBookshelfView(generics.RetrieveAPIView):
    queryset = Bookshelf.objects.all()
    serializer_class = BookshelfSerializer


class SpineListView(generics.ListAPIView):
    serializer_class = SpineListSerializer

    def get_queryset(self):
        bookshelf_pk = self.kwargs['bookshelf_pk']
        bookshelf = Bookshelf.objects.filter(id=bookshelf_pk)[0]
        queryset = Spine.objects.filter(bookshelf=bookshelf)
        return queryset
