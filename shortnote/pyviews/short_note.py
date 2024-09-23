from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from ..models import Note

@login_required
def loadnote(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "shortnote/notes/notelist.html", {
        "notes": notes
    })

@login_required
def addnote(request, note_id=None):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        if note_id:
            note = get_object_or_404(Note, id=note_id, user=request.user)
            note.title = title
            note.content = content
            note.save()
        else:
            Note.objects.create(user=request.user, title=title, content=content)
        
        return redirect("load_note")
    else:
        if note_id:
            note = get_object_or_404(Note, id=note_id, user=request.user)
            return render(request, "shortnote/notes/addnote.html", {"note": note})
        else:
            return render(request, "shortnote/notes/addnote.html")

@login_required
def delete_note(request, note_id):
    print("delete_note : ", note_id)
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect("load_note")
    elif request.method == "GET":
        return render(request, "shortnote/notes/confirm_delete.html", {"note": note})
    return redirect("load_note")
