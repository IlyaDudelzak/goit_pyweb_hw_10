from django import template
from django.db.models import Count
from ..models import Tag

register = template.Library()

sizes = [15, 25, 35] # min def max

@register.simple_tag
def top_tags():
    """
    Retrieve the top tags based on the number of associated quotes.

    :return: A list of tuples containing tags and their calculated sizes.
    :rtype: list[tuple[Tag, int]]
    """
    tags_with_count = list(Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes').all()[:10])

    try:
        max_count = tags_with_count[0].num_quotes if tags_with_count else 0
        min_count = tags_with_count[-1].num_quotes if tags_with_count else 0
    except:
        raise Exception(tags_with_count)

    tag_size_pairs = []
    for tag in tags_with_count:
        if max_count == min_count:
            size = sizes[1]
        else:
            size = sizes[0] + (tag.num_quotes - min_count) * (sizes[2] - sizes[0]) / (max_count - min_count)
        tag_size_pairs.append((tag, round(size)))

    return tag_size_pairs

# @register.simple_tag
# def top_tags():
#     tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
#     return tags
