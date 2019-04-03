from django.urls import path

from .views import (
    # BookListView,
    # BookDetailView,
    CreateBookshelfView,
)


urlpatterns = [
    # path('', BookListView.as_view()),
    path('create-bookshelf/', CreateBookshelfView.as_view()),
    # path('<pk>', BookDetailView.as_view()),
]
