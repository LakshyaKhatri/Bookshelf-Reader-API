from django.urls import path, re_path

from .views import (
    CreateBookshelfView,
    GetBookshelfView,
    SpineListView
)


urlpatterns = [
    # path('', BookListView.as_view()),
    path('create-bookshelf/', CreateBookshelfView.as_view()),
    path('bookshelf/<pk>/', GetBookshelfView.as_view()),
    re_path(r'spines/(?P<bookshelf_pk>\d+)/', SpineListView.as_view()),
]
