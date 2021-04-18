from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from auth_.models import User

@csrf_exempt
def auth(request):
    username = 'hasterun'
    password = 'bekbolat'
    user = authenticate(username=username, password=password)
    user = User.objects.get(id=2)
    print(user.password)
    if user is not None:
        # login(request, user)
        print(user)
    else:
        print('fail')

    return HttpResponse('ok')