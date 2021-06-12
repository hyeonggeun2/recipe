from django.urls import path

from recipes.views import refrigerator_view, add_view, add_ingredient_view, modify_ingredient_view, \
    delete_ingredient_view, recipe_view

app_name = 'recipes'

urlpatterns = [
    path('', refrigerator_view, name="refrigerator"),
    path('add/', add_view, name="add"),
    path('add_ingredient/', add_ingredient_view, name="add_ingredient"),
    path('modify/<int:ingredient>', modify_ingredient_view, name="modify_ingredient"),
    path('delete/<int:ingredient>', delete_ingredient_view, name="delete_ingredient"),
    path('recipe/', recipe_view, name="recipe"),
]
