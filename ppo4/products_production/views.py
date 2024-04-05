from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import connection
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Product_production
from .forms import Products_productionForm
from ingredients.models import Ingredients
from fproduct.models import Finishs

from django.db import connection


def sp_checkProducts(product_id, product_quantity):
    with connection.cursor() as cursor:
        sql = """
            DECLARE @returnValue int;
            EXEC sp_checkProducts2 @product_id = %s, @product_quantity = %s, @returnValue = @returnValue OUTPUT;
            SELECT @returnValue;
        """

        cursor.execute(sql, (product_id, product_quantity))
        result = cursor.fetchone()[0]

    return result == 1




def insert_product_production(product_id, quantity, date, employee_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC InsertProduction @product_id=%s, @product_quantity=%s, @Date=%s, @employee_id=%s",
                       [product_id, quantity, date, employee_id])



def update_raw_materials_and_products_after_production(product_id, quantity):
    with connection.cursor() as cursor:
        cursor.execute("EXEC UpdateRawMaterialsAndProductsAfterProduction @Product_id = %s, @Product_quantity = %s",
                       [product_id, quantity])



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
        product = form.cleaned_data['product']
        product_id = product.id
        print(product_id)
        product_quantity = form.cleaned_data['quantity']
        employee_id = form.cleaned_data.get('employees').id
        product_quantity = int(product_quantity)
        print(product_quantity)
        product_date_str = datetime.now().strftime('%Y-%m-%d')
        product_date = datetime.strptime(product_date_str, '%Y-%m-%d').date()

        is_enough_product = sp_checkProducts(product_id, product_quantity)

        print(is_enough_product)
        if is_enough_product:

            insert_product_production(product_id, product_quantity, product_date, employee_id)
            update_raw_materials_and_products_after_production(product_id, product_quantity)
            return redirect('products_production:index')
            # return super().form_valid(form)
        else:
            form.add_error(None, "Не хватает сырья.")
            return self.form_invalid(form)






class UpdateProducts_productionView(UpdateView):
    model = Product_production
    template_name = 'products_production-update.html'
    form_class = Products_productionForm
    success_url = reverse_lazy('products_production:index')


class DeleteProducts_productionView(DeleteView):
    model = Product_production
    template_name = 'products_production-delete.html'
    success_url = reverse_lazy('products_production:index')


