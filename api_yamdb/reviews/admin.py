"""reviews."""
from django.contrib import admin

from reviews.models import Category, Comment, Genres, Review, Title

for model in (Category, Genres, Comment, Review, Title):
    admin.site.register(model)
