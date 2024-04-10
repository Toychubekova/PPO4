from sqlite3 import IntegrityError

from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredients
from .forms import IngredientsForm, ProductForm
from fproduct.models import Finishs
from django.contrib import messages

def ingredients_list(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['Product_id']
            pr_id = Finishs.objects.get(Name=product)
            request.session['product_id'] = pr_id.id
            with connection.cursor() as cursor:
                cursor.execute("EXEC RawMatName @Product_id=%s", [pr_id.id])
                ingredients = cursor.fetchall()
    else:
        product_id = request.session.get('product_id')
        form = ProductForm(initial={'Product_id': product_id})
        if product_id:
            with connection.cursor() as cursor:
                cursor.execute("EXEC RawMatName @Product_id=%s", [product_id])
                ingredients = cursor.fetchall()
        else:
            ingredients = None
    context = {'ingredients': ingredients, 'form': form}
    return render(request, 'ingredients_list.html', context)


from django.db import connection
from django.shortcuts import render, redirect
from .forms import IngredientsForm
from django.contrib import messages

from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import IngredientsForm


from django.db import connection
from django.db.utils import IntegrityError

def ingredients_create(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['Product_id'].id
            raw_material_id = form.cleaned_data['RawMaterial_id'].id
            quantity = form.cleaned_data['Quantity']
            try:
                with connection.cursor() as cursor:
                    # Вызов хранимой процедуры с передачей параметров и получением значения @error
                    cursor.execute(
                        "DECLARE @error INT; EXEC CreateIngredient @Quantity=%s, @Product_id=%s, @RawMaterial_id=%s, @error=@error OUTPUT; SELECT @error;",
                        [quantity, product_id, raw_material_id])
                    error = cursor.fetchone()[0]
                if error == 0:
                    messages.error(request, 'Ингредиент с таким продуктом и сырьем уже существует.')
                else:
                    messages.success(request, 'Ингредиент успешно создан.')
            except Exception as e:

                return redirect('ingredients_list')
        else:
            messages.error(request, 'Форма заполнена некорректно. Пожалуйста, проверьте введенные данные.')
    else:
        form = IngredientsForm(initial={'Product_id': request.session.get('product_id')})
    return render(request, 'ingredients_form.html', {'form': form})

def ingredients_edit(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    if request.method == 'POST':
        form = IngredientsForm(request.POST, instance=ingredient)
        if form.is_valid():
            quantity = form.cleaned_data['Quantity']
            product_id = form.cleaned_data['Product_id'].id
            raw_material_id = form.cleaned_data['RawMaterial_id'].id
            with connection.cursor() as cursor:
                cursor.execute("EXEC Update_Ingredient @Ingredient_id=%s, @Quantity=%s, @Product_id=%s, @RawMaterial_id=%s",
                               [pk, quantity, product_id, raw_material_id])
            return redirect('ingredients_list')
    else:
        form = IngredientsForm(instance=ingredient)
    return render(request, 'ingredients_edit.html', {'form': form, 'ingredient': ingredient})

def ingredients_delete(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    with connection.cursor() as cursor:
        cursor.execute("EXEC DeleteIngredient @Ingredient_id=%s", [pk])
    return redirect('ingredients_list')
