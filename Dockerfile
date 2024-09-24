FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=capstone.settings

COPY .  /usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files (for Django)
RUN python manage.py collectstatic --noinput

# Expose the port used by Daphne
EXPOSE 8888

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8888", "capstone.asgi:application"]