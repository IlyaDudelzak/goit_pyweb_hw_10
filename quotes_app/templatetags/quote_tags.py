from django import template
from django.db.models import Count
from ..models import Tag

register = template.Library()

sizes = [15, 25, 35] # min def max

@register.simple_tag
def top_tags():
    # Annotate tags with the number of associated quotes
    tags_with_count = list(Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes').all()[:10])

    # Determine the maximum and minimum number of quotes
    # max_count = tags_with_count[0].num_quotes if tags_with_count else 0
    # min_count = tags_with_count[-1].num_quotes if tags_with_count else 0

    try:
        max_count = tags_with_count[0].num_quotes if tags_with_count else 0
        min_count = tags_with_count[-1].num_quotes if tags_with_count else 0
    except:
        raise Exception(tags_with_count)

    # Calculate sizes for each tag
    tag_size_pairs = []
    for tag in tags_with_count:
        if max_count == min_count:  # Avoid division by zero
            size = sizes[1]  # Default size
        else:
            size = sizes[0] + (tag.num_quotes - min_count) * (sizes[2] - sizes[0]) / (max_count - min_count)
        tag_size_pairs.append((tag, round(size)))

    return tag_size_pairs

# @register.simple_tag
# def top_tags():
#     # Получаем 10 тегов, которые чаще всего встречаются в цитатах
#     tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
#     return tags
