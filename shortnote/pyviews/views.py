from django.shortcuts import render
from ..models import Friend

def index(request):
    user = request.user
    print(user)
    return render(request, "shortnote/index.html")
