# Create your models here.
from django.db import models
from django.db.models.fields import AutoField
from django.utils.translation import gettext as _


class File(models.Models):
    id = models.AutoField(
        auto_created=True
    )
    filename = models.CharField(
        verbose_name=_("File name"),
        max_length=250
    )
    work_count = models.PositiveBigIntegerField(
        verbose_name=_("Number of works")
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True
    )

    def __str__(self) -> str:
        return f"{self.filename} - {self.work_count} songs"


class Contributor(models.Model):
    id = AutoField(
        auto_created=True,
        primary_key=False,
        unique=True
    )
    name = models.CharField(
        verbose_name=u"Contributors name",
        max_length=250,
        primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Work(models.Model):
    iswc = models.CharField(
        verbose_name=_("International Standard Musical Work Code"),
        max_length=11,
        primary_key=True
    )
    title = models.CharField(
        verbose_name=u"Music Title",
        max_length=250
    )
    contributors = models.ManyToManyField(
        Contributor,
        verbose_name=_("Contributors"), 
        blank=True
    )
    source = models.CharField(
        verbose_name=_("Metadata provider"),
        max_length=50
    )
    proprietary_id = models.PositiveIntegerField(
        verbose_name=_("Proprietary ID"),
        primary_key=False
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True
    )

    def __str__(self) -> str:
        contributors = "|".join(self.contributors.name)
        return f"{self.title} - {contributors}"
