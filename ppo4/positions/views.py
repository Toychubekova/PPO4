from multiprocessing import connection

from django.shortcuts import render, get_object_or_404, redirect
from .models import Positions
from .forms import PositionsForm

def list(request):
    positions = Positions.objects.all()
    return render(request, 'position_list.html', {'positions': positions})

def detail(request, pk):
    position = get_object_or_404(Positions, pk=pk)
    return render(request, 'position_detail.html', {'position': position})

def create(request):
    if request.method == 'POST':
        form = PositionsForm(request.POST)
        if form.is_valid():
            position_name = form.cleaned_data['Position']
            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_insert_position @Position=%s", [position_name])
            return redirect('position_list')
    else:
        form = PositionsForm()
    return render(request, 'position_form.html', {'form': form})

def edit(request, pk):
    position = get_object_or_404(Positions, pk=pk)
    if request.method == 'POST':
        form = PositionsForm(request.POST, instance=position)
        if form.is_valid():
            position_name = form.cleaned_data['Position']
            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_edit_position @pk=%s, @new_position=%s", [pk, position_name])
            return redirect('position_detail', pk=position.pk)
    else:
        form = PositionsForm(instance=position)
    return render(request, 'position_edit.html', {'form': form, 'position': position})
def delete(request, pk):
    position = get_object_or_404(Positions, pk=pk)
    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_del_position @id=%s", [pk])
    return redirect('position_list')

def detail(request, pk):
    position = get_object_or_404(Positions, pk=pk)
    return render(request, 'position_detail.html', {'position': position})

def create(request):
    if request.method == 'POST':
        form = PositionsForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.save()
            return redirect('position_detail', pk=position.pk)
    else:
        form = PositionsForm()
    return render(request, 'position_form.html', {'form': form})

def edit(request, pk):
    position = get_object_or_404(Positions, pk=pk)
    if request.method == 'POST':
        form = PositionsForm(request.POST, instance=position)
        if form.is_valid():
            position.save()
            return redirect('position_detail', pk=position.pk)
    else:
        form = PositionsForm(instance=position)
    return render(request, 'position_edit.html', {'form': form, 'position': position})

def delete(request, pk):
    position = get_object_or_404(Positions, pk=pk)
    position.delete()
    return redirect('position_list')
