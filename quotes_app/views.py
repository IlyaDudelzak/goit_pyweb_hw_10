from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.db.models import Count

from quotes_app.forms import AuthorForm, TagForm, QuoteForm
from quotes_app.models import Author, Tag, Quote

import requests
from bs4 import BeautifulSoup

ITEMS_PER_PAGE = 10
BASE_URL = 'https://quotes.toscrape.com'

def main(request):
    """
    Render the main page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered main page.
    :rtype: HttpResponse
    """
    return render(request, 'quotes_app/index.html')

@login_required
def author_create(request):
    """
    Handle the creation of a new author.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the main page or render the author creation form.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form_ = form.save(commit=False)
            form_.user = request.user
            form_.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'quotes_app/create.html', {'form': form})

    return render(request, 'quotes_app/create.html', {'form': AuthorForm()})


@login_required
def tag_create(request):
    """
    Handle the creation of a new tag.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the tag creation page or render the tag creation form.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form_ = form.save(commit=False)
            form_.user = request.user
            form_.save()
            return redirect(to='quotes_app:tag_create')
        else:
            return render(request, 'quotes_app/create.html', {'form': form})

    return render(request, 'quotes_app/create.html', {'form': TagForm()})


@login_required
def quote_create(request):
    """
    Handle the creation of a new quote.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the quote creation page or render the quote creation form.
    :rtype: HttpResponse
    """
    form = QuoteForm()
    print(form)
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quotes_app:quote_create')
        else:
            print(form.fields)

    return render(request, 'quotes_app/create.html', {"tags": tags, 'form': form})


def author_details(request, id):
    """
    Display details of a specific author.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param id: The ID of the author.
    :type id: int
    :return: Rendered author details page.
    :rtype: HttpResponse
    """
    item = Author.objects.filter(id=id)[0]
    print(item.name)
    return render(request, 'quotes_app/author/details.html', {"item": item})


def tag_details(request, tag, page=1):
    """
    Display details of a specific tag and its associated quotes.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param tag: The name of the tag.
    :type tag: str
    :param page: The page number for pagination.
    :type page: int
    :return: Rendered tag details page.
    :rtype: HttpResponse
    """
    vars = {"notfound": False, "name": tag}
    try:
        tag = Tag.objects.get(name=tag)
        vars["tag"] = tag
        quotes = Quote.objects.filter(tags__name=tag.name)
        vars["quotes"] = quotes[((page - 1) * ITEMS_PER_PAGE):(page * ITEMS_PER_PAGE)]
        vars["page"] = page
        hp = int(len(quotes) / ITEMS_PER_PAGE) + 1
        vars["err"] = (page < 1 or page > hp)
        vars["ok"] = not vars["err"]
        vars["lpe"] = ((page - 1) > 0)
        vars["hpe"] = ((page + 1) <= hp)
    except Tag.DoesNotExist:
        vars["notfound"] = True
    
    return render(request, 'quotes_app/tag/details.html', vars)



def quote_details(request, id):
    """
    Display details of a specific quote.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param id: The ID of the quote.
    :type id: int
    :return: Rendered quote details page.
    :rtype: HttpResponse
    """
    item = Quote.objects.filter(pk=id)
    return render(request, 'quotes_app/quote/details.html', {"item": item})

def author_page(request, page):
    """
    Display a paginated list of authors.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param page: The page number for pagination.
    :type page: int
    :return: Rendered author page.
    :rtype: HttpResponse
    """
    vars = {}
    items = Author.objects.all()
    vars["items"] = items[((page - 1) * ITEMS_PER_PAGE):(page * ITEMS_PER_PAGE)]
    vars["page"] = page
    hp = int(len(items) / ITEMS_PER_PAGE) + 1
    vars["err"] = (page < 1 or page > hp)
    vars["ok"] = not vars["err"]
    vars["lpe"] = ((page - 1) > 0)
    vars["hpe"] = ((page + 1) <= hp)
        
    return render(request, 'quotes_app/author/page.html', vars)


def tag_page(request, page):
    """
    Display a paginated list of tags.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param page: The page number for pagination.
    :type page: int
    :return: Rendered tag page.
    :rtype: HttpResponse
    """
    vars = {}
    tags = list(Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes').all()[:10])
    vars["tags"] = tags[((page - 1) * ITEMS_PER_PAGE):(page * ITEMS_PER_PAGE)]
    vars["page"] = page
    hp = int(len(tags) / ITEMS_PER_PAGE) + 1
    vars["err"] = (page < 1 or page > hp)
    vars["ok"] = not vars["err"]
    vars["lpe"] = ((page - 1) > 0)
    vars["hpe"] = ((page + 1) <= hp)
        
    return render(request, 'quotes_app/tag/page.html', vars)

def quote_page(request, page):
    """
    Display a paginated list of quotes.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param page: The page number for pagination.
    :type page: int
    :return: Rendered quote page.
    :rtype: HttpResponse
    """
    vars = {}
    quotes = Quote.objects.all()
    vars["quotes"] = quotes[((page - 1) * ITEMS_PER_PAGE):(page * ITEMS_PER_PAGE)]
    vars["page"] = page
    hp = int(len(quotes) / ITEMS_PER_PAGE) + 1
    vars["err"] = (page < 1 or page > hp)
    vars["ok"] = not vars["err"]
    vars["lpe"] = ((page - 1) > 0)
    vars["hpe"] = ((page + 1) <= hp)
        
    return render(request, 'quotes_app/quote/page.html', vars)

def parsing_view(request):
    """
    Display all quotes with their associated authors and tags.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered parsing view page.
    :rtype: HttpResponse
    """
    quotes = Quote.objects.select_related('author').prefetch_related('tags').all()
    return render(request, 'quotes_app/parsing.html', {'quotes': quotes})

@user_passes_test(lambda u: u.is_superuser)
def parse_quotes(request):
    """
    Parse quotes from an external website and save them to the database.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the parsing view page.
    :rtype: HttpResponse
    """
    url = BASE_URL
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote_block in soup.find_all('div', class_='quote'):
            text = quote_block.find('span', class_='text').get_text()
            author_name = quote_block.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote_block.find_all('a', class_='tag')]

            # Save author if not already in the database
            author, created = Author.objects.get_or_create(name=author_name)
            if created:
                author_link = BASE_URL + quote_block.find('a', href=True)['href']
                author_response = requests.get(author_link)
                author_soup = BeautifulSoup(author_response.text, 'html.parser')
                author.born_date = author_soup.find('span', class_='author-born-date').get_text()
                author.born_location = author_soup.find('span', class_='author-born-location').get_text()
                author.description = author_soup.find('div', class_='author-description').get_text()
                # print(author.name)
                # print(author.born_date)
                # print(author.born_location)
                # print(author.description)
                author.save()

            # Save quote
            quote, _ = Quote.objects.get_or_create(text=text, author=author)

            # Save tags
            for tag_name in tags:
                print(tag_name)
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

        # Check for the next page
        next_page = soup.find('li', class_='next')
        url = BASE_URL + next_page.find('a')['href'] if next_page else None

    return redirect('quotes_app:parsing')

