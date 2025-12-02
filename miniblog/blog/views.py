import json
import sys
from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Author, Blog, Comment

from django.views import generic


def printRequest(request):
    # print(request.__dict__, file=sys.stderr) # print(request) -> <WSGIRequest: GET '/blog/'> 🌝

    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"GET parameters: {request.GET}")
    print(f"POST parameters: {request.POST}")
    print(f"Headers: {request.headers}")
    print(f"User: {request.user}") # If authentication is set up
    print(f"Body: {request.body}")
    for key, value in request.META.items():
        print(f"{key}: {value}")
    return HttpResponse('See the terminal!')

def index(request):
    """View function for home page of site."""
    num_of_blogs = Blog.objects.all().count()
    num_of_authors = Author.objects.all().count()
    num_of_comments = Comment.objects.all().count()

    context = {
        "num_of_authors": num_of_authors,
        "num_of_blogs": num_of_blogs, 
        "num_of_comments": num_of_comments
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# function views but has serialization issues and lot of repeated code need to be written
# => use class views extending generic view from django, as shown next
# def all_authors(request):
#     return HttpResponse(Author.objects.all())

class BlogListView(generic.ListView):
    model=Blog

class AuthorListView(generic.ListView):
    model=Author

class BlogDetailView(generic.DetailView):
    model=Blog

# functional implementation for above
# def book_detail_view(request, pk):
#     try:
#         blog = Blog.objects.get(pk=pk)
#     except Blog.DoesNotExist:
#         raise Http404('Blog does not exist')

#     return render(request, 'blog/blog_detail.html', context={'blog': blog})

class AuthorDetailView(generic.DetailView):
    model=Author
