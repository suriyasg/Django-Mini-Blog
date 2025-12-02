from django.db import models
from django.urls import reverse
import uuid # Required for unique book instances

# Create your models here.

class Author(models.Model):
    """Model representing an author."""
    user_name = models.CharField(max_length=256, unique=True)

    class Meta:
        ordering = ['user_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user_name}'

class Blog(models.Model):
    """Model representing a Blog."""
    # We assume blog can only have one author, but authors can have multiple blogs.
    # Author as a string rather than object because it hasn't been declared yet in file.
    
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library"
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # if author delete his account then blogs are deleted
    posted_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=10000, help_text="Write your blog")

    class Meta:
        ordering = ['-posted_on'] # ordering = ['posted_on'] will sort ascending


    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this blog."""
        # TODO : Check what reverse function is for
        return reverse('blog-detail', args=[str(self.id)])

class Comment(models.Model):

    """Model representing a comment under a blog."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular comment")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE) # if blog get deleted comments refering blog also get deleted
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # if user account get deleted comments by them also get deleted
    commented_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=500, help_text="Write your comment")

    class Meta:
        ordering = ['-commented_on']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.blog.title})'