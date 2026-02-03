import requests
from django.shortcuts import get_object_or_404, render, redirect
from django.core.cache import cache
from django.contrib import messages
from .models import TodoItem


# Create your views here.
def getPhoneData():
    data = cache.get('phone_data')
    if not data:
        url = "https://dummyjson.com/users"  
        response = requests.get(url)
        data = response.json()
        cache.set('phone_data', data, timeout=300)  # Cache for 5 minutes
        return data
        
def home(request):
    return render(request, "home.html")


def all(request):
    todo_item = TodoItem.objects.all()
    return render(request, "all.html", {"todos": todo_item})


def add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")

        if not title or len(title) > 100:
            messages.error(
                request, "Title is required and must be less than 100 characters."
            )
            return render(request, "add.html")
        else:
            TodoItem.objects.create(title=title, description=description)
            messages.success(request, "To do item added successfully!")
            return redirect("all")
    return render(request, "add.html")


def detail(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)
    return render(request, "detail.html", {"item": item})


def edit(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")

        if not title or len(title) > 100:
            messages.error(
                request, "Title is required and must be less than 100 characters."
            )
            return render(request, "edit.html", {"item": item})
        else:
            item.title = title
            item.description = description
            item.save()
            messages.success(request, "To do item updated successfully!")
            return redirect("all")
    return render(request, "edit.html", {"item": item})


def delete(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)
    item.delete()
    messages.success(request, "To do item deleted successfully!")
    return redirect("all")


def phoneList(request):
    try:
       
        data = getPhoneData()
        context = {"data": data}
        return render(request, "phoneList.html", context)
    except requests.RequestException as e:
        return render(
            request,
            "phoneList.html",
            {"data": None, "error": str(e)},
        )

def phoneDetail(request, item_id):
     
     
     try:
        data = getPhoneData()
        item_data = next((item for item in data if str(item["id"]) == str(item_id)))
        context = {"data": item_data}
        return render(request, "phoneDetail.html", context)
     except requests.RequestException as e:
            return render(
                request,
                "phoneDetail.html",
                {"data": None, "error": str(e)},
            )