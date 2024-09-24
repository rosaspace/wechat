from datetime import datetime
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from ..models import Friend, User


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "shortnote/profile/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "shortnote/profile/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request,
                "shortnote/profile/register.html",
                {"message": "Passwords must match."},
            )

        # Check if email already exists in the database
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "shortnote/profile/register.html",
                {"message": "Email already registered."},
            )

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "shortnote/profile/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shortnote/profile/register.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user

        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.bio = request.POST.get("bio", user.bio)
        user.location = request.POST.get("location", user.location)
        birth_date = request.POST.get("birth_date", user.birth_date)

        # Validate birth_date format
        try:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            user.birth_date = birth_date
        except ValueError:
            messages.error(request, "Birth date must be in YYYY-MM-DD format.")
            return render(
                request,
                "shortnote/profile/edit_profile.html"
            )

        if "profile_picture" in request.FILES:
            profile_picture = request.FILES["profile_picture"]
            fs = FileSystemStorage()
            file_extension = profile_picture.name.split(".")[-1]

            # image path
            file_path = (
                f"shortnote/static/user_images/"
                f"{user.username}.{file_extension}"
            )
            if fs.exists(file_path):
                fs.delete(file_path)
            fs.save(file_path, profile_picture)
            
            # DB path
            user.profile_image = (
                f"static/user_images/{user.username}.{file_extension}"
            )

        user.save()

        messages.success(request, "Profile updated successfully.")
        return HttpResponseRedirect(reverse("edit_profile"))
    else:
        user_data = {
            "user": request.user,
            "profile_image": (
                request.user.profile_image.url
                if request.user.profile_image
                else None
            ),
        }
        return render(
            request,
            "shortnote/profile/edit_profile.html",
            user_data
        )


@login_required
def friends(request):
    user = request.user
    friends = Friend.objects.filter(user=user)
    friend_data = []

    for friend in friends:
        friend_user = friend.friend
        friend_info = {
            "id": friend_user.id,
            "username": friend_user.username,
            "email": friend_user.email,
            "bio": getattr(friend_user, "bio", ""),
            "location": getattr(friend_user, "location", ""),
            "profile_image": (
                friend_user.profile_image.url
                if friend_user.profile_image
                else None
            ),
        }
        friend_data.append(friend_info)
    return render(
        request, "shortnote/profile/friends.html", {"friends": friend_data}
    )

@login_required
def friendsData(request):
    if request.method == "GET":
        try:
            user = request.user
            friends = (
                Friend.objects.filter(user=user)
                .select_related("friend")
                .exclude(friend=user)
            )
            friend_list = [
                {
                    "username": friend.friend.username,
                    "email": friend.friend.email,
                    "profile_image": (
                        friend.friend.profile_image.url
                        if friend.friend.profile_image
                        else None
                    ),
                }
                for friend in friends
            ]

            return JsonResponse({"success": True, "friends": friend_list})
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": str(e)},
                status=500
            )

    return JsonResponse(
        {"success": False, "error": "Invalid request method"},
        status=400
    )

# abandon
@login_required
def selfData(request):
    if request.method == "GET":
        try:
            user = request.user
            self_data = {
                "username": user.username,
                "email": user.email,
                "profile_image": (
                    user.profile_image.url
                    if user.profile_image
                    else None
                ),
            }

            return JsonResponse({"success": True, "self": self_data})
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": str(e)},
                status=500
            )

    return JsonResponse(
        {"success": False, "error": "Invalid request method"},
        status=400
    )   


@login_required
def add_friend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse(
                {"state": False, "message": "Email is required."}
            )

        try:
            friend_user = User.objects.get(email=email)

            if friend_user == request.user:
                return JsonResponse(
                    {
                        "state": False,
                        "message": "You cannot add yourself as a friend.",
                    }
                )

            friend, created = Friend.objects.get_or_create(
                user=request.user, friend=friend_user
            )

            if created:
                # Also add the reverse relationship
                Friend.objects.get_or_create(
                    user=friend_user, friend=request.user
                )
                return JsonResponse(
                    {"state": True, "message": "Friend added successfully."}
                )
            else:
                return JsonResponse(
                    {
                        "state": False,
                        "message": "This user is already your friend.",
                    }
                )

        except User.DoesNotExist:
            return JsonResponse(
                {
                    "state": False,
                    "message": "User with this email does not exist.",
                }
            )

    return JsonResponse(
        {"state": False, "message": "Invalid request method."}
    )
