# Rooydad-Negar

Rooydad-Negar is a Django-based project designed to manage events for a university. It provides an easy-to-use interface for organizing and tracking university events.

---

## Technologies Used

### Backend
- **Django**: A high-level Python web framework for rapid development and clean design.
- **django-jalali**: A Django extension for using Jalali (Persian) dates in your models and forms.
- **Pillow**: A Python Imaging Library used for image processing.
- **sorl-thumbnail**: A thumbnail library for Django that helps with image thumbnailing.
- **requests**: A Python library for making HTTP requests.

### Frontend
- **Tailwind CSS**: A utility-first CSS framework for building custom designs.
- **Django Templates**: Django's built-in templating engine for rendering HTML.

---

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites
- Python 3.x
- pip (Python package manager)
- virtualenv (for creating virtual environments)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Fasa-UPC/rooydad-negar.git
   cd rooydad-negar
   ```
<br>

2. **Set Up a Virtual Environment**
   - Create a virtual environment:
  ```bash
   virtualenv env
   ```
   - Activate the virtual environment:
       - On macOS/Linux:
       ```bash
       source env/bin/activate
       ```
       - On Windows:
       ```bash
       env\Scripts\activate
       ```
<br>

3. **Install Dependencies**
   - Install the required packages from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
<br>

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
<br>

5. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```
<br>

6. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
<br>

7. Open up your browser and go to `127.0.0.1:8000`
<br>

8. The admin panel is available at `127.0.0.1:8000/admin/`
---

For any queries or issues, feel free to open an issue in the repository.
