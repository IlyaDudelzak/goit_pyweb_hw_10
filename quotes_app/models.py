from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    """
    Model representing an author with details such as name, description, and birth information.
    """
    name = models.CharField(max_length=50, null=False, unique=True, validators=[RegexValidator('^[a-zA-Z0-9_ ]+$', inverse_match=True)])
    description = models.TextField(null=False)
    born_date = models.CharField(max_length=50, null=False)
    born_location = models.CharField(max_length=150, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return f"{self.name}"

class Tag(models.Model):
    """
    Model representing a tag associated with quotes.
    """
    name = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1, validators=[RegexValidator('^[a-zA-Z0-9_ ]+$', inverse_match=True)])

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"
    
class Quote(models.Model):
    """
    Model representing a quote with an author and associated tags.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    text = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)