from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from products_sale.models import Product_sale
from products_sale.forms import Products_saleForm

from raw_sale.models import Budget


class Products_saleView(ListView):
    model = Product_sale
    template_name = 'products_sale/products_sale-list.html'
    context_object_name = 'products_sale'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_sale'] = Product_sale.objects.all().select_related('product')
        context['budget'] = Budget.objects.first()

        return context

class CreateProducts_saleView(CreateView):
    model = Product_sale
    template_name = 'products_sale/products_sale-create.html'
    form_class = Products_saleForm
    success_url = reverse_lazy('products_sale:index')

    def form_valid(self, form):
        product_sale = form.save(commit=False)
        budget = Budget.objects.first()

        if product_sale.quantity > product_sale.product.Quantity:
            form.add_error(None, 'Недостаточно продукта на складе.')
            return self.form_invalid(form)

        product_quantity = product_sale.product.Quantity  # Правильный атрибут из модели Finishs
        product_amount = product_sale.product.Amount  # Правильный атрибут из модели Finishs

        product_sale.amount = (product_amount / product_quantity) * product_sale.quantity

        product_sale.product.Quantity -= product_sale.quantity
        product_sale.product.Amount -= product_sale.amount
        product_sale.product.save()

        sale_sum = product_sale.amount * (1 + budget.percentage / 100)
        product_sale.amount = sale_sum
        budget.quantity += sale_sum
        budget.save()
        product_sale.product.save()

        return super().form_valid(form)


class UpdateProducts_saleView(UpdateView):
    model = Product_sale
    template_name = 'products_sale/products_sale-update.html'
    form_class = Products_saleForm
    success_url = reverse_lazy('products_sale:index')


class DeleteProducts_saleView(DeleteView):
    model = Product_sale
    template_name = 'products_sale/products_sale-delete.html'
    success_url = reverse_lazy('products_sale:index')