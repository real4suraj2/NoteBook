from django.contrib import admin
from .models import NoteCategory, NoteSeries, Note,UserProfile
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.
class NoteAdmin(admin.ModelAdmin):
	fieldsets = [
	("Title/date",{"fields":["note_title","note_published"]}),
	("URL",{"fields":["note_slug"]}),
	("Series",{"fields":["note_series"]}),
	("Content",{"fields":["note_content"]}),
	]
	formfield_overrides = {
		models.TextField : { 'widget': TinyMCE() }
	}
admin.site.register(NoteCategory)
admin.site.register(NoteSeries)
admin.site.register(UserProfile)
admin.site.register(Note,NoteAdmin)