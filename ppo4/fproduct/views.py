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
            raw = form.save()
            return redirect('FProduct_detail', pk=raw.pk)
    else:
        form = FinishsForm()
    return render(request, 'FProduct_form.html', {'form': form})

def FProduct_edit(request, pk):
    raw = get_object_or_404(Finishs, pk=pk)
    if request.method == 'POST':
        form = FinishsForm(request.POST, instance=raw)
        if form.is_valid():
            raw = form.save()
            return redirect('FProduct_detail', pk=raw.pk)
    else:
        form = FinishsForm(instance=raw)
    return render(request, 'FProduct_edit.html', {'form': form, 'Finish': raw})

def FProduct_delete(request, pk):
    raw = get_object_or_404(Finishs, pk=pk)
    raw.delete()
    return redirect('FProduct_list')
