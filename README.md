# Chat Application

**Description**: This project is a real-time chat application where users can register, log in, edit their information, add friends, and chat with them in real time using WebSocket. The project is built using Django, Django Channels, Daphne, and Channels-Redis, and supports both local development and Docker-based deployment.

## Table of Contents
- Features
- Technologies Used
- Development Setup
- Deployment
- WebSocket Support
- Contributing
- License

## Features
- **User Registration**: Create a new account.
- **User Login**: Log in to your account.
- **Edit User Information**: Update your profile details.
- **Friend Management**: Add, view, and manage friends.
- **Real-time Chat**: Send and receive messages with friends in real time using WebSocket.


## Technologies Used

- **Python**: The programming language used for server-side logic.
- **JavaScript**: Used for client-side interactivity.
- **Django**: The core web framework.
- **Django Channels**: Extends Django to handle WebSockets, allowing for real-time features.
- **Daphne**: The ASGI server that serves Django Channels.
- **Channels-Redis**: Provides Redis as the backing store for Channels, enabling real-time communication.
- **SQLite**: Default database for development.

## Development Setup

### Local Development

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Create a virtual environment**:

   ```py
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```py
   pip install -r requirements.txt
   ```

4. **Apply migrations and create manager**:

   ```py
   python manage.py migrate
   python manage.py createsuperuser  # Create an admin user
   ```
   
5. **Run Redis (required for Channels-Redis)**:

    Ensure Redis is running locally. You can install Redis using your package manager:

    ```bash
    sudo apt-get install redis-server
    ```

    Then start Redis:

    ```bash
    sudo service redis-server start
    ```
    
8. **Add your IP address to ALLOWED_HOSTS in settings.py**

    ```bash
   ALLOWED_HOSTS = ["129.80.201.9", "localhost", "127.0.0.1"]
   ```
   
6. **Run the development server**:

    ```bash
    daphne -b 0.0.0.0 -p 8000 yourproject.asgi:application
    ```
    
7. **Or Run python**

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### Docker Development

1. **Install Docker**

   ```py
   sudo apt update // Update the package database
   sudo apt install docker.io // Install Docker
   sudo systemctl start docker // Start Docker
   sudo systemctl enable docker // Enable it to run at startup
   ```

2. **Install docker-compose**

   ```py
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose // download the latest version of Docker Compose
   sudo chmod +x /usr/local/bin/docker-compose // make the Docker Compose binary executable
   docker-compose --version // Check if Docker Compose is installed correctly by verifying the version
   ```

3. **(Optional)Allow non-root users to run Docker**

   ```py
   sudo usermod -aG docker $USER // Add your user to the docker group
   newgrp docker // Log out and log back in
   docker run hello-world // After logging back in, verify that Docker can run without sudo by running
   ```

4. **Build and start the container using docker compose**

   ```py
   docker-compose up --build
   ```

   This will start the Django development server, Redis, and Daphne.

5. **Stop the container**

   ```py
   docker-compose down
   ```

6. **Access the application**:

    The application can be accessible at `http://localhost:8000`.
    
## Deployment
For production deployment, consider using a proper ASGI server setup with Daphne and Channels-Redis. You'll also need to configure static files and media storage, as well as secure your environment with HTTPS and appropriate security settings.

## WebSocket Support

This project supports WebSocket communication using Django Channels, Daphne, and Redis. You can test WebSocket functionality by accessing specific routes that utilize the WebSocket consumers defined in your app.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

1. Fork the repo and create your branch from main.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code follows the code style guidelines.

## License
This project is licensed under the MIT License.

```bash
Replace `yourusername/yourproject` with your actual GitHub repository link and `yourproject` with the actual name of your Django project. This template covers the basic setup and instructions for both local development and Docker-based deployment.
```

## Publish Link
https://onlinetools.life/

Account Pass
user1 user1
user2 user2
user3 user3

