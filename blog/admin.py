from .models import TextEditor
from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE


class TextEditorAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(TextEditor, TextEditorAdmin)
