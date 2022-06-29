import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('person_name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\". \"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class RoleType(models.TextChoices):
    director = 'director', _('director')
    writer = 'writer', _('writer')
    actor = 'actor', _('actor')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', verbose_name = _('Person for creating'), on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=RoleType.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' '

    class Meta:
        db_table = "content\". \"person_film_work"
        verbose_name = _('PersonFilmwork')
        verbose_name_plural = _('PersonFilmworks')
        indexes = [
            models.Index(fields=['film_work', 'person', 'role']),
            models.Index(fields=['film_work'], name='film_work_person_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'], name='unique_person_role'
            )
        ]


class GenreType(models.TextChoices):
    movie = 'movie', _('movie')
    tv_show = 'tv_show', _('tv_show')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', verbose_name = _('Genres for creating'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' '

    class Meta:
        db_table = "content\". \"genre_film_work"
        verbose_name = _('GenreFilmwork')
        verbose_name_plural = _('GenreFilmworks')
        indexes = [
            models.Index(fields=['film_work', 'genre']),
            models.Index(fields=['film_work'], name='film_work_genre_idx'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='unique_genre')
        ]


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('film_title'), max_length=255)
    description = models.TextField(_('film_description'), blank=True)
    creation_date = models.DateField(_('film_creation_date'))
    rating = models.FloatField(
        _('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.TextField(_('type'), choices=GenreType.choices, null=True)
    genres = models.ManyToManyField(
        Genre, related_name='genres', through='GenreFilmwork'
    )  # после ревью  related_name='genres',
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
