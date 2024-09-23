from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json

from datetime import datetime

from ..models import Friend, Chat, User


@login_required
def send_chat(request, friendname):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            chat_content = data.get("chat_content")
            if not chat_content:
                return JsonResponse(
                    {"success": False, "error": "Chat content is required"},
                    status=400
                )

            timestamp = timezone.now()
            friend_user = User.objects.get(username=friendname)
            chat = Chat.objects.create(
                sender=request.user,
                receiver=friend_user,
                content=chat_content,
                timestamp=timestamp,
            )

            chat.save()

            return JsonResponse(
                {"success": True, "message": "Chat saved successfully"}
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON data"},
                status=400
            )
        except User.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Friend not found"},
                status=404
            )
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
def load_chat(request):
    if request.method == "GET":
        try:
            user = request.user
            all_chat_data = (
                Chat.objects.filter(Q(sender=user) | Q(receiver=user))
                .order_by("timestamp")
                .values(
                    "content",
                    "timestamp",
                    "sender__username",
                    "receiver__username"
                )
            )

            all_chat_data = list(all_chat_data)

            for chat in all_chat_data:
                chat["sender"] = chat.pop("sender__username")
                chat["receiver"] = chat.pop("receiver__username")
                chat["timestamp"] = chat["timestamp"].isoformat()

            return JsonResponse({"success": True, "chat_data": all_chat_data})
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
def load_new_chat(request):
    if request.method == "GET":
        try:
            last_timestamp = request.GET.get("last_timestamp")

            if last_timestamp:
                last_timestamp = datetime.fromisoformat(last_timestamp)
            else:
                last_timestamp = datetime.min

            new_messages = Chat.objects.filter(
                Q(sender=request.user) | Q(receiver=request.user),
                timestamp__gt=last_timestamp,
            ).order_by("timestamp")

            all_new_chat_data = []
            for message in new_messages:
                chat_data = {
                    "content": message.content,
                    "sender": message.sender.username,
                    "receiver": message.receiver.username,
                    "timestamp": message.timestamp.isoformat(),
                }
                all_new_chat_data.append(chat_data)
            return JsonResponse(
                {"success": True, "chat_data": all_new_chat_data}
            )
        except ValueError:
            return JsonResponse(
                {"success": False, "error": "Invalid timestamp format"},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": str(e)},
                status=500
            )

    return JsonResponse(
        {"success": False, "error": "Invalid request method"},
        status=400
    )
