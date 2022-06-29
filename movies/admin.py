from django.contrib import admin
from .models import Genre
from .models import GenreFilmwork
from .models import Filmwork
from .models import Person
from .models import PersonFilmwork
from django.utils.translation import gettext_lazy as _


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = (
        'title',
        'description',
    )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (
        PersonFilmworkInline,
        GenreFilmworkInline,
    )
    list_filter = ('type',)
    search_fields = (
        'title',
        'description',
    )
    list_display = (
        'title',
        'type',
        'get_genres',
        'creation_date',
        'rating',
    )
    list_prefetch_related = [
        'genres',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'
