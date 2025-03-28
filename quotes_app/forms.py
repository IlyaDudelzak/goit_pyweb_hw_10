from django.forms import ModelChoiceField, ModelForm, CharField, ModelMultipleChoiceField, DateField, Select, TextInput, DateInput, CheckboxSelectMultiple, SelectMultiple
from django.utils.translation import gettext as _

from .models import Author, Tag, Quote


class AuthorForm(ModelForm):

    name = CharField(label=_("author_name"), max_length=50, required=True, widget=TextInput())
    born_date = CharField(label=_("author_birth_date"), max_length=50, required=True, widget=TextInput())
    born_location = CharField(label=_("author_birth_location"), max_length=50, required=True, widget=TextInput())
    description = CharField(label=_("author_description"), required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['name', 'description', 'born_date', 'born_location']

class TagForm(ModelForm):

    name = CharField(label=_("tag_name"), min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']

class QuoteForm(ModelForm):
    author = ModelChoiceField(label=_("quote_author"), queryset=Author.objects.all(), required=True, widget=Select())
    text = CharField(label=_("quote_text"), min_length=10, required=True, widget=TextInput())
    tags = ModelMultipleChoiceField(label=_("select_tags"), queryset=Tag.objects.all(), required=True, widget=SelectMultiple())

    class Meta:
        model = Quote
        fields = ['author', 'text', 'tags']