from django.shortcuts import redirect,render
from django.http import HttpResponse
from lists.models import Item

# how does this get to lists.views?
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text','')
        # shortcut for Item(), assign properties in param, and .save()
        Item.objects.create(text=new_item_text) 
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html',{'items': items})
