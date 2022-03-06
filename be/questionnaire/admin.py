from django.contrib import admin

from questionnaire.models import Category, Field, VotedField

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'max_field', 'current_field',
                    'created_at', 'updated_at', 'started_at', 'ended_at')
    readonly_fields = ('id', 'created_at', 'updated_at')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Category, CategoryAdmin)


class FieldAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'total_vote', 'image')
    readonly_fields = (['id'])

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Field, FieldAdmin)


class VotedFieldAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'voted_time', 'is_voted')
    readonly_fields = (['id'])

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(VotedField, VotedFieldAdmin)
