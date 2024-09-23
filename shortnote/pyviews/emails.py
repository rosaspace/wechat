import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse


def send_email_hotmail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            verification_code = data.get('verification_code')

            if not email or not verification_code:
                return JsonResponse({"state": False, "message": "Email and verification code are required"}, status=400)

            subject = 'Register WeChat Verification Email'
            email_to = [email]
            email_from = settings.DEFAULT_FROM_EMAIL

            message = 'This is a register email sent from WeChat.'
            message += f"\n\nHere is your verification code: {verification_code}"
            message += "\n\nPlease return to the page to enter the verification code."

            send_mail(subject, message, email_from, email_to)
            return JsonResponse({"state": True, "message": "Email sent to Hotmail"})
        except json.JSONDecodeError:
            return JsonResponse({"state": False, "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"state": False, "message": f"Failed to send email: {str(e)}"}, status=500)
    else:
        return JsonResponse({"state": False, "message": "Invalid request method"}, status=405)
