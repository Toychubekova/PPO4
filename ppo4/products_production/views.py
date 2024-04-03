from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.db import connection
from django.utils import timezone
from .forms import Products_productionForm
from .models import Product_production

class Products_productionView(ListView):
    model = Product_production
    template_name = 'products_production-list.html'
    context_object_name = 'products_production'


class CreateProducts_productionView(CreateView):
    model = Product_production
    template_name = 'products_production-create.html'
    form_class = Products_productionForm
    success_url = reverse_lazy('products_production:index')

    def form_valid(self, form):
        product = form.instance.product
        product_quantity = form.cleaned_data['quantity']
        employees_id = form.cleaned_data['employees']


        # Устанавливаем текущую дату и время для поля "date"
        form.instance.date = timezone.now()

        with connection.cursor() as cursor:
            cursor.execute(
                "DECLARE @enough_product BIT; EXEC @enough_product = sp_checkProducts @product_id=%s, @product_quantity=%s; SELECT @enough_product",
                [product.id, product_quantity]
            )
            enough_product = cursor.fetchone()

            if enough_product is not None and enough_product[0] == 0:
                form.add_error(None, "There is not enough of this product available.")
                return self.form_invalid(form)

            cursor.execute(
                "EXEC InsertProductProd @product_id=%s, @quantity=%s, @employees_id=%s",
                [product.id, product_quantity, employees_id.id]
            )

            # Вызываем хранимую процедуру InsertProductProd для вставки данных
            cursor.execute(
                "EXEC sp_updateProductAndRawMaterials @product_id=%s, @product_quantity=%s",
                [product.id, product_quantity]
            )

        return redirect('products_production:index')

class UpdateProducts_productionView(UpdateView):
    model = Product_production
    template_name = 'products_production-update.html'
    form_class = Products_productionForm
    success_url = reverse_lazy('products_production:index')

class DeleteProducts_productionView(DeleteView):
    model = Product_production
    template_name = 'products_production-delete.html'
    success_url = reverse_lazy('products_production:index')