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
