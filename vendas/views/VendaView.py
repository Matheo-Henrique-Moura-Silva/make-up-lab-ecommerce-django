from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

def testando(request):
    return HttpResponse("ESTAMOS NO MODULO VENDA!!!")
