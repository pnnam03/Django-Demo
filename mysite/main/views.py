from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList
# Create your views here.


def home(response):
    return render(response, "main/home.html", {"lists" : ToDoList.objects.all()})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"] # decrypt name
            #check_existance = ToDoList.objects.get(name=n).count()

            t = ToDoList(name = n)
            t.save()
    form = CreateNewList()
    return render(response, "main/create.html", {"form" : form, "lists" : ToDoList.objects.all()})

def list(response, id=1):
    cur_list = ToDoList.objects.get(id = id)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in cur_list.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif response.POST.get("add"):
            txt = response.POST.get("new")
            if len(txt) > 0:
                cur_list.item_set.create(text = txt, complete = False)
            else:
                print("invalid")
        elif response.POST.get("delete"):
            del_id = int(response.POST.get("delete"))
            ToDoList.objects.get(id = del_id).delete()
            return redirect('/list')

    return render(response, "main/list.html", {"list" : cur_list} )

def list_all(response):
    if response.method == "POST":
        if response.POST.get("delete"):
            del_id = int(response.POST.get("delete"))
            ToDoList.objects.get(id = del_id).delete()
        elif response.POST.get("new-name"):
            Id = int(response.POST.get("rename-btn"))
            new_name = response.POST.get("new-name")
            ToDoList.objects.filter(id=Id).update(name=new_name)

    return render(response, "main/list_all.html", {"lists" : ToDoList.objects.all(), "list_cnt" : ToDoList.objects.count()})