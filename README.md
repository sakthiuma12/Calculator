# Simple Calculator

**Ex.No:** 06

**Date:** __________

## Aim

To design and develop a calculator using Django, HTML, CSS, and JavaScript that performs addition, subtraction, multiplication, and division.

## Algorithm

1. Create a Django project and a calculator app.
2. Create an HTML page for the calculator interface and display.
3. Use CSS to arrange and style the calculator buttons and display.
4. Use JavaScript to handle digit, operator, clear, and calculate button clicks.
5. Send each calculation to the Django app and validate the inputs.
6. Display the result and save the calculation in the SQLite database.
7. Test the arithmetic operations and error handling.

## Project names

- **Django project:** `calculator_project`
- **Django app:** `calculator`
- **Virtual environment:** `.venv`
- **Database:** SQLite

## Setup on Windows

Run these commands from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations calculator
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` after starting the development server.

## Result

Thus, a Django-based calculator was designed and developed to perform basic arithmetic operations and retain recent calculations.
