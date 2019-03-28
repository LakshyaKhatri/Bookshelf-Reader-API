from django.urls import path, re_path

from .views import BookListView, BookDetailView


urlpatterns = [
    path('', BookListView.as_view()),
    path('<pk>', BookDetailView.as_view())
]
