from django.urls import path
from . import views

app_name = 'quotes_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('parsing/', views.parsing_view, name='parsing'),
    path('parse-quotes/', views.parse_quotes, name='parse_quotes'),
    path('author/create', views.author_create, name='author_create'),
    path('tag/create', views.tag_create, name='tag_create'),
    path('quote/create', views.quote_create, name='quote_create'),
    path('author/<int:id>', views.author_details, name='author_details'),
    path('tag/<str:tag>', views.tag_details, name='tag_details'),
    path('tag/<str:tag>/page/<int:page>', views.tag_details, name='tag_details_page'),
    path('quote/<int:id>', views.quote_details, name='quote_details'),
    path('author/page/<int:page>', views.author_page, name='author_page'),
    path('tag/page/<int:page>', views.tag_page, name='tag_page'),
    path('quote/page/<int:page>', views.quote_page, name='quote_page'),
    path('test', views.test),
]