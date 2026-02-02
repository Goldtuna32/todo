from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import TodoItem

# Create your views here.

def home(request):
    return render(request, 'home.html')

def all(request):
    todo_item = TodoItem.objects.all()
    return render(request, 'all.html', {'todos': todo_item})

def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if not title or len(title) > 100:
            messages.error(request, 'Title is required and must be less than 100 characters.')
            return render(request, 'add.html')
        else:
            TodoItem.objects.create(title=title, description=description)
            messages.success(request, 'To do item added successfully!')
            return redirect('all')
    return render(request, 'add.html')

def detail(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)
    return render(request, 'detail.html', {'item': item})

def edit(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if not title or len(title) > 100:
            messages.error(request, 'Title is required and must be less than 100 characters.')
            return render(request, 'edit.html', {'item': item})
        else:
            item.title = title
            item.description = description
            item.save()
            messages.success(request, 'To do item updated successfully!')
            return redirect('all')
    return render(request, 'edit.html', {'item': item})

def delete(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)
    item.delete()
    messages.success(request, 'To do item deleted successfully!')
    return redirect('all')