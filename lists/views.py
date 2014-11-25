from django.shortcuts import render


# how does this get to lists.views?
def home_page(request):
    return render(request, 'home.html')
