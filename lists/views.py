from django.shortcuts import render
from django.http import HttpResponse

#how does this get to lists.views?
def home_page(request):
	return HttpResponse('<html><title>To-Do Lists</title></html>')

