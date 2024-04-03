from django.db import connection

from django.shortcuts import render, get_object_or_404, redirect
from .models import Finishs
from .forms import FinishsForm

def FProduct_list(request):
    raws = Finishs.objects.all()
    return render(request, 'FProduct_list.html', {'Finishs': raws})

def FProduct_detail(request, pk):
    raw = get_object_or_404(Finishs, pk=pk)
    return render(request, 'FProduct_detail.html', {'Finish': raw})

def FProduct_create(request):
    if request.method == 'POST':
        form = FinishsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            quantity = form.cleaned_data['Quantity']
            amount = form.cleaned_data['Amount']
            unit_id = form.cleaned_data['Unit_id'].id

            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_insert_FProduct @Name=%s, @Quantity=%s, @Amount=%s, @Unit_id=%s", [name, quantity, amount, unit_id])

            return redirect('FProduct_list')
    else:
        form = FinishsForm()
    return render(request, 'FProduct_form.html', {'form': form})

def FProduct_edit(request, pk):
    fproduct = get_object_or_404(Finishs, pk=pk)
    if request.method == 'POST':
        form = FinishsForm(request.POST, instance=fproduct)
        if form.is_valid():
            name = form.cleaned_data['Name']
            quantity = form.cleaned_data['Quantity']
            amount = form.cleaned_data['Amount']
            unit_id = form.cleaned_data['Unit_id'].id
            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_update_FProduct @pk=%s, @Name=%s, @Quantity=%s, @Amount=%s, @Unit_id=%s", [pk, name, quantity, amount, unit_id])
            return redirect('FProduct_list')
    else:
        form = FinishsForm(instance=fproduct)
    return render(request, 'FProduct_edit.html', {'form': form, 'Finish': fproduct})


from django.shortcuts import get_object_or_404, redirect
from .models import Finishs


def FProduct_delete(request, pk):
    # Находим объект Finishs по его идентификатору
    finish = get_object_or_404(Finishs, pk=pk)

    # Проверяем, был ли отправлен POST-запрос (запрос на удаление объекта)
    if request.method == 'POST':
        # Удаляем объект из базы данных
        finish.delete()
        # После успешного удаления объекта, перенаправляем пользователя на страницу списка объектов
        return redirect('FProduct_list')

    # Если запрос был GET, просто возвращаем шаблон подтверждения удаления с информацией об объекте
    return render(request, 'FProduct_delete_confirm.html', {'Finish': finish})

