from django.urls import path
from .pyviews import views
from .pyviews import auth_views
from .pyviews import chat
from .pyviews import emails
from .pyviews import short_note

urlpatterns = [
    path("", views.index, name="index"),
    path("send_email_hotmail", emails.send_email_hotmail, name="send_email_hotmail"),

    path("login", auth_views.login_view, name="login"),
    path("logout", auth_views.logout_view, name="logout"),
    path("register", auth_views.register, name="register"),
    path("edit_profile", auth_views.edit_profile, name="edit_profile"),
    
    path("friends", auth_views.friends, name="friends"),
    path("friendsData", auth_views.friendsData, name="friendsData"),
    path("selfData", auth_views.selfData, name="selfData"), # abandon
    path("add_friend", auth_views.add_friend, name="add_friend"),

    path("load_note", short_note.loadnote, name="load_note"),
    path("add_note", short_note.addnote, name="add_note"),
    path("edit_note/<int:note_id>", short_note.addnote, name="edit_note"),
    path("delete_note/<int:note_id>", short_note.delete_note, name="delete_note"),

    path("load_chat", chat.load_chat, name="load_chat"),
    path("load_new_chat", chat.load_new_chat, name="load_new_chat"), # abandon
    path("send_chat/<str:friendname>", chat.send_chat, name="send_chat"),
]
