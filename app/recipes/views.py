import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect

# Create your views here.
from members.models import User
from recipes.models import Ingredient, MyIngredientInfo


def refrigerator_view(request):
    user = User.objects.get(username=request.user.username)
    freeze = MyIngredientInfo.objects.filter(refrigerator=user.refrigerator, ingredient__state="freeze")
    freeze = sorted(freeze, key=lambda x: x.left_days())
    cold = MyIngredientInfo.objects.filter(refrigerator=user.refrigerator, ingredient__state="cold")
    cold = sorted(cold, key=lambda x: x.left_days())

    data = {
        "freeze": freeze,
        "cold": cold
    }

    return render(request, 'refrigerator/main.html', data)


def add_view(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        ingredient = Ingredient.objects.get(name=request.POST['ingredient'], state=request.POST['state'])
        quantity = request.POST['quantity']
        date = request.POST['date']

        MyIngredientInfo.objects.create(ingredient=ingredient, refrigerator=user.refrigerator, quantity=quantity,
                                        buy_date=date)

        return redirect('recipes:refrigerator')
    else:
        state = request.GET['state']
        data = {
            "state": request.GET['state'],
            "ingredients": Ingredient.objects.filter(state=state).order_by('name'),
        }
        return render(request, 'refrigerator/add.html', data)


def add_ingredient_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        shelf_life = request.POST['shelf_life']
        state = request.POST['state']
        Ingredient.objects.create(name=name, shelf_life=shelf_life, state=state)

        response = redirect('recipes:add')
        response['Location'] += f'?state={state}'
        return response
    else:
        data = {
            "state": request.GET['state']
        }
        return render(request, 'refrigerator/add_ingredient.html', data)


def modify_ingredient_view(request, ingredient):
    my_ingredient = MyIngredientInfo.objects.get(pk=ingredient)
    if request.method == 'POST':
        my_ingredient.quantity = request.POST["quantity"]
        my_ingredient.save()
        return redirect('recipes:refrigerator')
    else:
        data = {
            "ingredient": my_ingredient,
        }
        return render(request, 'refrigerator/modify.html', data)


def delete_ingredient_view(request, ingredient):
    MyIngredientInfo.objects.get(pk=ingredient).delete()
    return redirect('recipes:refrigerator')


def recipe_view(request):
    # 크롤링
    base_url = 'https://www.10000recipe.com/recipe/list.html?q='

    selected = request.GET.getlist('ingredient', None)

    # 자동추천
    if len(selected) == 0:
        user = User.objects.get(username=request.user.username)
        ingredients = MyIngredientInfo.objects.filter(refrigerator=user.refrigerator)
        ingredients = sorted(ingredients, key=lambda x: x.left_days())

        selected = [ingredients[0].ingredient.name, ingredients[1].ingredient.name]

    query = "%2B".join(selected)
    search_url = base_url + query

    response = requests.get(search_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.select('.rcp_m_list2 .common_sp_list_li')

    if len(items) == 0:
        data = {
            "items": None,
        }
    else:
        recipe_list = []
        for item in items:
            temp_dict = {}
            temp_dict["title"] = item.select_one('.common_sp_caption_tit').get_text()
            temp_dict["link"] = 'https://www.10000recipe.com/' + item.select_one('a.common_sp_link')['href']
            temp_dict["img"] = item.select_one('.common_sp_link > img')['src']
            recipe_list.append(temp_dict)

        data = {
            "ingredient": "+".join(selected),
            "items": recipe_list,
        }

    print(data)
    return render(request, 'refrigerator/recipe.html', data)
