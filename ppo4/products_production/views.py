from django.core.exceptions import ValidationError
from django.db.models import Case, F, Sum, Value, When
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Product_production
from .forms import Products_productionForm
from ingredients.models import Ingredients
from fproduct.models import Finishs
from products_production.models import Product_production


class Products_productionView(ListView):
    model = Product_production
    template_name = 'products_production-list.html'
    context_object_name = 'products_production'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_production'] = Product_production.objects.all().select_related('product')

        return context

class CreateProducts_productionView(CreateView):
    model = Product_production
    template_name = 'products_production-create.html'
    form_class = Products_productionForm
    success_url = reverse_lazy('products_production:index')

    def form_valid(self, form):
        product_id = form.instance.product_id
        product_quantity = form.cleaned_data['quantity']


        ingredients = Ingredients.objects.filter(Product_id=product_id).select_related('RawMaterial_id')
        total_sum = 0
        enough_raw_materials = True

        for ingredient in ingredients:
            need_materials = ingredient.Quantity * product_quantity
            need_materials_sum = (
                                             ingredient.RawMaterial_id.Amount / ingredient.RawMaterial_id.Quantity) * need_materials

            if ingredient.RawMaterial_id.Amount < need_materials_sum:
                enough_raw_materials = False
                form.add_error(None,
                               f"There is not enough product to produce a given amount of product {ingredient.RawMaterial_id.Name}. "
                               f"Required: {need_materials_sum}, In stock: {ingredient.RawMaterial_id.Amount}")

            total_sum += need_materials_sum

        # Если нет достаточного количества сырья, возвращаем ошибку
        if not enough_raw_materials:
            return self.form_invalid(form)


        product = Finishs.objects.get(id=product_id)
        product.Quantity += product_quantity
        product.Amount += total_sum
        product.save()


        for ingredient in ingredients:
            need_materials = ingredient.Quantity * product_quantity
            need_materials_sum = (
                                             ingredient.RawMaterial_id.Amount / ingredient.RawMaterial_id.Quantity) * need_materials
            ingredient.RawMaterial_id.Quantity -= need_materials
            ingredient.RawMaterial_id.Amount -= need_materials_sum
            ingredient.RawMaterial_id.save()

        # Добавляем общую сумму к объекту формы перед сохранением
        form.instance.amount = total_sum

        return super().form_valid(form)

class UpdateProducts_productionView(UpdateView):
    model = Product_production
    template_name = 'products_production-update.html'
    form_class = Products_productionForm
    success_url = reverse_lazy('products_production:index')


class DeleteProducts_productionView(DeleteView):
    model = Product_production
    template_name = 'products_production-delete.html'
    success_url = reverse_lazy('products_production:index')