from django.contrib import admin
from App_Course.models import Course, Tag, Prerequisite, Learning, Video

# Register your models here.

#to show the Tag, Prerequisite and Learning models in Course Model in dhnago admin
class TagAdmin(admin.TabularInline):
    model = Tag

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite

class LearningAdmin(admin.TabularInline):
    model = Learning

class VideoAdmin(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, PrerequisiteAdmin, LearningAdmin, VideoAdmin]

admin.site.register(Course, CourseAdmin)
#admin.site.register(Tag)
#admin.site.register(Prerequisite)
#admin.site.register(Learning)
#admin.site.register(Video)