from django.contrib import admin

# Register your models here.
from .models import Course,lessons,Person,watch_later,category
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}
admin.site.register(Course,CourseAdmin)
admin.site.register(lessons)
admin.site.register(Person)
admin.site.register(watch_later)
admin.site.register(category)