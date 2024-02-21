from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredients
from .forms import IngredientsForm, ProductForm
from fproduct.models import Finishs


def ingredients_list(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['Product_id']
            pr_id = Finishs.objects.get(Name=product)

            request.session['product_id'] = pr_id.id

            ingredients = Ingredients.objects.filter(Product_id=product)
    else:
        product_id = request.session['product_id']
        form = ProductForm(initial={'Product_id': product_id})
        ingredients = Ingredients.objects.filter(Product_id=product_id)

    context = {'ingredients': ingredients, 'form': form}
    return render(request, 'ingredients_list.html', context)


def ingredients_detail(request, pk):
    sale = get_object_or_404(Ingredients, pk=pk)
    return render(request, 'ingredients_detail.html', {'ingredient': sale})

def ingredients_create(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            sale = form.save()
            return redirect('ingredients_list')
    else:
        form = IngredientsForm(initial={'Product_id': request.session['product_id']})
    return render(request, 'ingredients_form.html', {'form': form})

def ingredients_edit(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    if request.method == 'POST':
        form = IngredientsForm(request.POST, instance=ingredient)
        if form.is_valid():
            ingredient = form.save()
            return redirect('ingredients_list')
    else:
        form = IngredientsForm(instance=ingredient)
    return render(request, 'ingredients_edit.html', {'form': form, 'ingredients': ingredient})

def ingredients_delete(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    ingredient.delete()
    return redirect('ingredients_list')