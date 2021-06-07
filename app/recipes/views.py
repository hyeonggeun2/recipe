from django.shortcuts import render, redirect

# Create your views here.
from members.models import User
from recipes.models import Ingredient, MyIngredientInfo


def refrigerator_view(request):
    user = User.objects.get(username=request.user.username)
    freeze = MyIngredientInfo.objects.filter(refrigerator=user.refrigerator, ingredient__state="freeze")
    cold = MyIngredientInfo.objects.filter(refrigerator=user.refrigerator, ingredient__state="cold")

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

        # freeze = MyIngredientInfo.objects.filter(refrigerator=user.refrigerator, ingredient__state="freeze")
        # cold = MyIngredientInfo.objects.filter(refrigerator=user.refrigerator, ingredient__state="cold")
        #
        # data = {
        #     "freeze": freeze,
        #     "cold": cold
        # }
        return redirect('recipes:refrigerator')
    else:
        state = request.GET['state']
        data = {
            "state": request.GET['state'],
            "ingredients": Ingredient.objects.filter(state=state),
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
