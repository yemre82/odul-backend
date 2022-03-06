from django.urls import path

from questionnaire.views import add_category, add_field, edit_category, edit_field, get_all_categories, get_all_current_categories, remove_category, remove_field, vote_field


urlpatterns = [
    path("add-category",add_category),
    path("add-field",add_field),
    path("edit-category",edit_category),
    path("edit-field",edit_field),
    path("remove-category",remove_category),
    path("remove-field",remove_field),
    path("get-all-current-categories",get_all_current_categories),
    path("get-all-categories",get_all_categories),
    path("vote-field",vote_field)
]
