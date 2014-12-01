from django.shortcuts import redirect,render
from django.http import HttpResponse
from lists.models import Item, List

# how does this get to lists.views?
def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html')

def view_list(request,list_id):
    list_ = List.objects.get(id=list_id)
    return render(request,'list.html',{'list':list_})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],owningList = list_)
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request,list_id):
    list_ = List.objects.get(id = list_id)
    Item.objects.create(text=request.POST['item_text'],owningList = list_)
    return redirect('/lists/%d/' % (list_.id,))

