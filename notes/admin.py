# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from django.contrib import admin

from . import models

admin.site.register(models.Note)
admin.site.register(models.User)
admin.site.register(models.Log)
admin.site.register(models.Entry)
admin.site.register(models.EntryData)