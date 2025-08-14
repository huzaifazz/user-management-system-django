
# Django User Management System

This is a feature-rich Django web application for user management, post creation, and role-based access control. It supports user registration, authentication, custom user roles (admin, moderator, editor, user), profile management with avatars and social links, and more.

## Features

- User registration, login, and logout
- User profiles with avatar, bio, and social links
- Custom roles: Admin, Moderator, Editor, User
- Role-based permissions for posts and comments
- Superuser/admin can edit any user's profile and role
- Create, edit, and delete posts
- Comment on superuser posts
- Responsive UI with Bootstrap 5
- MySQL database support

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/huzaifazz/user-management-system-django.git
cd user-management-system-django
```

- **Create and activate a virtual environment:**

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# Or
source .venv/bin/activate  # On Mac/Linux
```

- **Install dependencies:**

```bash
pip install -r requirements.txt
```

- **Configure your database in `website/settings.py`** (default is MySQL, update credentials as needed).

- **Apply migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

- **Create a superuser:**

```bash
python manage.py createsuperuser
```

- **Run the development server:**

```bash
python manage.py runserver
```

1. **Visit** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage

- Register a new user or log in as superuser.
- Edit your profile, upload an avatar, and add social links.
- Admins can edit any user's profile and assign roles.
- Create posts and comment on superuser posts.
- Role-based permissions are enforced throughout the app.

## Technologies Used

- Django 5
- MySQL
- Bootstrap 5
- Pillow (for image uploads)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
