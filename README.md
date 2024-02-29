# Django-Cms

This Django CMS project features admin and author roles, providing admins full content management and authors the ability to CRUD their content. The repository includes user registration, admin seeding, and basic CRUD operations, along with content search functionality.


## Introduction

Welcome to our Content Management System (CMS) project! This system is designed to provide a robust platform for managing and organizing digital content with a focus on flexibility and user-friendly interaction.

In today's digital age, the need for an efficient and customizable content management system is crucial for businesses, bloggers, and content creators. Our CMS offers a comprehensive solution for both administrators and authors, ensuring seamless content creation, management, and search capabilities.

## Features
    -User Roles: Two distinct user roles, Admin and Author, each with specific privileges to ensure secure and controlled access.
    -Authentication and Authorization: A robust authentication system for user registration and login, coupled with authorization mechanisms to control access to content.
    -Content Operations: Authors can create, edit, and delete their content, while admins have the authority to manage all content across the platform.
    -Search Functionality: Users can easily search for content based on terms found in titles, bodies, summaries, and categories.

## Installation

1. Clone the repository:

   ```bash
   git clone (https://github.com/Akhtar21yr/Django-CMS.git))
   cd cms

2. Create and Activate a Virtual Environment:
python -m venv venv
source venv/bin/activate  # for Windows- use venv\Scripts\activate


3. Install the Project Dependencies:
pip install -r requirements.txt


4. Apply Migrations:
python manage.py migrate


5. Start the Development Server:
python manage.py runserver


6. Access CMS Project:
Visit http://localhost:8000/ in your web browser.

7. Usage
Admin Panel: Access the admin panel at http://localhost:8000/admin/ to manage users and content items.

8. API Endpoints: Explore the API endpoints to interact with the application programmatically.

9. Seed Data
You can use the django-seed package to seed your database with sample data. Refer to the cms_app\management\commands\seeds.py file for more details on seeding.
you can run a command python manage.py makemigration seed to add admin
