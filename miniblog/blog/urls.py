from django.urls import path
from blog import views


urlpatterns = [
    path('',  view=views.index, name='index'),
    path('blogs/', view=views.BlogListView.as_view(), name='blogs'),
    path('blogs/<uuid:pk>', view=views.BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<uuid:pk>/comment', view=views.add_comment, name='add-comment'),
    # path('blogs/comment/<uuid:pk>/', view=views.edit_comment, name='edit-comment'),
    # path('blogs/<uuid:pk>', view=views.book_detail_view, name='blog-detail'),
    path('authors/', view=views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', view=views.AuthorDetailView.as_view(), name='author-detail'),
    path('print/', view=views.printRequest, name="print")
]