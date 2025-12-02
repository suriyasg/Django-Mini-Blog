from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse

from blog.forms import CommentForm
from .models import Author, Blog, Comment
from django.contrib.auth import get_user_model
User = get_user_model()

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect

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

    # Number of visits to this view, as counted in the session variable.
    num_of_visits = request.session.get('num_of_visits', 0)
    num_of_visits += 1
    request.session['num_of_visits'] = num_of_visits

    context = {
        "num_of_authors": num_of_authors,
        "num_of_blogs": num_of_blogs, 
        "num_of_comments": num_of_comments,
        'num_of_visits': num_of_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# function views but has serialization issues and lot of repeated code need to be written
# => use class views extending generic view from django, as shown next
# def all_authors(request):
#     return HttpResponse(Author.objects.all())

class BlogListView(generic.ListView):
    model=Blog
    paginate_by = 1

class AuthorListView(LoginRequiredMixin, generic.ListView):
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


# function-based views, the easiest way to restrict access to your functions is to 
# apply the login_required decorator to your view function
# or manually check request object in view
# request.user.is_authenticated


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model=Author

@login_required
def add_comment(request, pk):
    print(request.method)
    blog = get_object_or_404(Blog, pk=pk)
    user = get_object_or_404(User, username=request.user.username)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        print(request.method == "POST")
        # Create a form instance and populate it with data from the request (binding):
        form = CommentForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            content = form.cleaned_data["content"]
            new_comment = Comment(blog=blog, content=content, user=user)
            new_comment.save()
            return redirect('blog-detail', pk=pk)
    
    else:
        print(request.method == "POST")
        form = CommentForm()


    context = {
        'form': form,
        'blog' : blog
    }
    return render(request, 'blog/add_comment.html', context)

def edit_comment(request, pk):
    pass
