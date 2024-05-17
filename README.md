# Django REST API with Posts and Blocked Users

## Project Overview

This project is a Django REST API that allows users to create, read, update, and delete posts. Additionally, users can block and unblock other users. Email notifications are sent when a new post is created. The project also includes pagination, custom permissions, and email configurations.

## Features

1. **User Authentication**: Uses Django's built-in User model for authentication.
2. **Post Management**: Users can create, retrieve, update, and delete their own posts.
3. **Blocked Users**: Users can block and unblock other users.
4. **Email Notifications**: Sends email notifications to the author when a new post is created.
5. **Pagination**: Implements pagination for listing posts.
6. **Custom Permissions**: Ensures users can only manage their own posts.
7. **Filtering and Searching**: Allows filtering posts by title, body, and author.

## API Endpoints

### Posts
- **GET /api/posts/**: Returns a list of all posts.
- **POST /api/posts/**: Creates a new post owned by the authenticated user.
- **GET /api/posts/<int:pk>/**: Returns a single post by ID.
- **PUT /api/posts/<int:pk>/**: Updates a single post owned by the authenticated user.
- **DELETE /api/posts/<int:pk>/**: Deletes a single post owned by the authenticated user (soft delete).

### Blocked Users
- **GET /api/blocked-users/**: Returns the list of blocked users.
- **POST /api/blocked-users/**: Blocks a user.
- **DELETE /api/blocked-users/<int:pk>/**: Unblocks a user.

## Setup and Installation

### Prerequisites
- Python 3.7+
- Django 3.0+
- Django REST framework

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

### Email Configuration

Configure your email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
EMAIL_USE_TLS = True
#Replace the placeholders with your actual email credentials.

##Usage
Creating a Post
To create a post, send a POST request to /api/posts/ with the title, body, and author fields.

##Listing Posts
To list all posts, send a GET request to /api/posts/. Pagination is enabled by default.

##Updating a Post
To update a post, send a PUT request to /api/posts/<int:pk>/ with the updated data.

##Deleting a Post
To delete a post, send a DELETE request to /api/posts/<int:pk>/.

##Blocking a User
To block a user, send a POST request to /api/blocked-users/ with the user and blocked_user fields.

##Unblocking a User
To unblock a user, send a DELETE request to /api/blocked-users/<int:pk>/.

##Custom Permissions
IsOwnerOrReadOnly: Ensures that users can only update or delete their own posts. Superusers have full access.

Signals:Sends an email notification to the author when a new post is created.

Pagination:Configured to paginate posts with a default page size of 10.

Filtering and Searching:Users can filter posts by title, body, and author using query parameters.
