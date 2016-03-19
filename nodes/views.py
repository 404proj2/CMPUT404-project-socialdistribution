from django.http import HttpResponse
from django.shortcuts import render
from nodes.models import Node

# Create your views here.

def show_nodes(request):
	return HttpResponse("Nodes page not implemented yet.")
