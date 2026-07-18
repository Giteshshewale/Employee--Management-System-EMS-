# Employee Management System (Django + MySQL)

A full-featured Employee Management System built with Django, covering
authentication, role-based access control, employee CRUD, search/filter/
pagination, file uploads, attendance, leave management, salary, dashboard
statistics, reports/export, email notifications, and an admin panel.

## Features implemented

| # | Module | Status |
|---|--------|--------|
| 1 | Authentication (Register/Login/Logout/Change Password/Forgot Password) | ✅ |
| 2 | Dashboard with stat cards | ✅ |
| 3 | Department CRUD | ✅ |
| 4 | Employee CRUD (all spec fields) | ✅ |
| 5 | Search (name, ID, dept, email, city) | ✅ |
| 6 | Filter (department, status) | ✅ |
| 7 | Pagination | ✅ |
| 8 | Employee Profile page | ✅ |
| 9 | Profile Photo Upload (jpg/png/jpeg) | ✅ |
| 10 | Resume Upload (pdf/doc/docx) | ✅ |
| 11 | Salary Module (Basic/HRA/DA/Bonus/Total) | ✅ |
| 12 | Attendance (Present/Absent/Half Day) | ✅ |
| 13 | Leave Management (Apply/Approve/Reject) | ✅ |
| 14 | Admin Panel (Django admin, fully wired) | ✅ |
| 15 | Reports (Employee/Department/Attendance/Salary) | ✅ |
| 16 | Export (CSV, Excel, PDF) | ✅ |
| 17 | Email (Welcome email, Leave approval email) | ✅ |
| 18 | User Roles (Admin/HR/Employee) | ✅ |
| 19 | Notifications | ✅ |

## Tech stack

Python 3.11+, Django 5, MySQL (SQLite by default for zero-setup local dev),
Bootstrap 5, Bootstrap Icons.

## Project structure

```
ems/
├── manage.py
├── requirements.txt
├── employee_project/      # settings, root urls, wsgi/asgi
├── accounts/               # custom user, auth views, roles, decorators
├── departments/            # Department CRUD
├── employees/               # Employee CRUD, search/filter/pagination, uploads
├── attendance/              # Attendance tracking
├── leaves/                  # Leave application/approval workflow
├── salaries/                 # Salary records
├── notifications/            # In-app notifications
├── dashboard/                # Dashboard stats
├── reports/                  # Reports + CSV/Excel/PDF export
├── templates/                # All HTML templates (Bootstrap 5)
├── static/css/style.css      # Custom styling
└── media/                    # Uploaded profile photos & resumes
```

## 1. Setup (local machine — this needs internet access, which the build
environment here did not have, so run these steps yourself)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

> `mysqlclient` requires MySQL's dev headers to build. On Ubuntu/Debian:
> `sudo apt-get install default-libmysqlclient-dev build-essential pkg-config`
> On macOS: `brew install mysql-client` (and export the pkg-config path it prints).
> If that's a hassle while learning, skip MySQL for now — the project runs
> perfectly on SQLite out of the box (see below), and you can switch to MySQL
> later once the app works end-to-end.

### Option A — Quick start with SQLite (recommended to begin with)

No extra setup needed. `employee_project/settings.py` already points at SQLite.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — you'll be redirected to the login page.
Log in with the superuser you just created, or register a new account.

### Option B — Switch to MySQL (matches the original spec)

1. Create the database:
   ```sql
   CREATE DATABASE employee_management_db CHARACTER SET utf8mb4;
   ```
2. In `employee_project/settings.py`, comment out the `DATABASES` SQLite
   block and uncomment the MySQL block just below it, filling in your
   MySQL username/password.
3. Run the same migrate/createsuperuser/runserver commands as above.

## 2. Assigning roles

By default, new registrations pick a role (`admin` / `hr` / `employee`) on
the registration form. In practice you'll usually want to:

1. Create a superuser (`python manage.py createsuperuser`) — this account
   automatically has full admin access regardless of its `role` field.
2. Log into `/admin/` and set the `role` field for other users as needed,
   or manage it from the registration form.
3. To let an "employee" role user see their **own** profile, link their
   user account to an `Employee` record: open the employee in
   `/admin/employees/employee/`, and set the `user` field to their login
   account.

## 3. Where things live

- **Uploaded files** go to `media/profile_photos/` and `media/resumes/`.
- **Emails** print to your terminal by default (`EMAIL_BACKEND` = console
  backend) — perfect for seeing "Welcome" and "Leave approved/rejected"
  emails while developing. Switch to real SMTP in `settings.py` when ready.
- **Reports** live under `/reports/` (Admin/HR only) — CSV always works;
  Excel needs `openpyxl` and PDF needs `reportlab` (both already in
  `requirements.txt`).

## 4. Suggested Git workflow (for your GitHub repo / resume)

```bash
git init
git add .
git commit -m "Initial commit: full Employee Management System"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Commit as you go feature-by-feature (auth, then departments, then employees,
etc.) rather than one giant commit — a clean commit history is itself a
resume signal.

## 5. Suggested learning/extension order

The core of every module above is implemented, but here are natural next
steps if you want to deepen it further for your resume:

1. Add Django REST Framework endpoints (the spec lists this as "later").
2. Add unit tests (`python manage.py test`) for models and views.
3. Add class-based views for at least one module, to show you know both.
4. Deploy it (Render, Railway, PythonAnywhere, or a VPS + Nginx + Gunicorn)
   and put the live link in your resume/README.
5. Add Signals (e.g. auto-create a Notification via `post_save` on Employee
   instead of doing it in the view) — the spec lists Signals as optional.

## 6. Default page map

| URL | Purpose |
|---|---|
| `/accounts/register/` | Register |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/accounts/change-password/` | Change password |
| `/accounts/forgot-password/` | Forgot password |
| `/dashboard/` | Dashboard |
| `/departments/` | Department list/CRUD |
| `/employees/` | Employee list/search/filter/CRUD |
| `/attendance/` | Attendance list/mark |
| `/leaves/` | Leave list/apply/approve/reject |
| `/salaries/` | Salary list/add |
| `/notifications/` | Notifications |
| `/reports/` | Reports + export |
| `/admin/` | Django admin panel |
