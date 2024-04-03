from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredients
from .forms import IngredientsForm, ProductForm
from fproduct.models import Finishs

def ingredients_create(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredients_list')
    else:
        form = IngredientsForm()
    return render(request, 'ingredients_create.html', {'form': form})




def ingredients_list(request):
    context = {}
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['Product_id']
            pr_id = Finishs.objects.get(Name=product)
            request.session['product_id'] = pr_id.id

            # Call the stored procedure FilterIngredientsByProduct
            with connection.cursor() as cursor:
                cursor.execute("EXEC RawMatName @Product_id=%s", [pr_id.id])
                rows = cursor.fetchall()  # Получить результаты з
                context['ingredients'] = rows

        context['form'] = form

        return render(request, 'ingredients_list.html', context)
    else:
        product_id = request.session.get('product_id')
        if product_id is not None:
            ingredients = Ingredients.objects.filter(Product_id=product_id)
        else:
            ingredients = None

        form = ProductForm(initial={'Product_id': product_id})
        context['form'] = form

    return render(request, 'ingredients_list.html', context)


def ingredients_edit(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    if request.method == 'POST':
        form = IngredientsForm(request.POST, instance=ingredient)
        if form.is_valid():
            quantity = form.cleaned_data['Quantity']
            product_id = form.cleaned_data['Product_id'].id
            raw_material_id = form.cleaned_data['RawMaterial_id'].id
            with connection.cursor() as cursor:
                cursor.execute("EXEC Update_Ingredient @Ingredient_id=%s, @Quantity=%s, @Product_id=%s, @RawMaterial_id=%s", [pk, quantity, product_id, raw_material_id])
            return redirect('ingredients_list')
    else:
        form = IngredientsForm(instance=ingredient)
    return render(request, 'ingredients_edit.html', {'form': form, 'ingredient': ingredient})


def ingredients_delete(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    with connection.cursor() as cursor:
        cursor.execute("EXEC DeleteIngredient @Ingredient_id=%s", [pk])
    return redirect('ingredients_list')
