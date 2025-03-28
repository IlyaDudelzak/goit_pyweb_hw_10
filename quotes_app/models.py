from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True, validators=[RegexValidator('^[a-zA-Z0-9_ ]+$', inverse_match=True)])
    description = models.TextField(null=False)
    born_date = models.CharField(max_length=50, null=False)
    born_location = models.CharField(max_length=150, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return f"{self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1, validators=[RegexValidator('^[a-zA-Z0-9_ ]+$', inverse_match=True)])

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"
    
class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    text = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)