from django.shortcuts import render


def index(request):
    friend = request.GET.get('friend')
    context = {'friend': friend} if friend else {}
    return render(request, "shortnote/index.html", context)
