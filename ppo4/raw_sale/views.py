from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.db.models import F
from raw_sale.models import Budget, RawSale
from raw_sale.forms import MaterialPurchaseForm


class MaterialPurchaseView(ListView):
    model = RawSale
    template_name = 'material_purchase/materials_purchase-list.html'
    context_object_name = 'material_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['raw_sale'] = RawSale.objects.all().select_related('material')
        context['budget'] = Budget.objects.first()
        return context


class CreateMaterialPurchaseView(CreateView):
    model = RawSale
    template_name = 'material_purchase/material_purchase-create.html'
    form_class = MaterialPurchaseForm
    success_url = reverse_lazy('raw_sale:index')

    @transaction.atomic
    def form_valid(self, form):
        # Получить экземпляр покупки материала
        raw_sale = form.save(commit=False)

        # Проверить, достаточно ли бюджета
        budget = Budget.objects.first()
        if raw_sale.amount <= budget.quantity:
            # Уменьшить сумму бюджета
            budget.quantity -= raw_sale.amount
            budget.save()

            # Увеличить количество материала в наличии
            material = raw_sale.material
            material.Quantity += raw_sale.quantity
            material.save()

            # Увеличить сумму закупки
            raw_sale.save()
            material.Amount += raw_sale.amount
            material.save()

            return super().form_valid(form)
        else:
            # Если бюджет недостаточен, показать сообщение об ошибке
            form.add_error(None, "There is not enough budget for this purchase.")
            return self.form_invalid(form)