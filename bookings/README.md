# Serenity Salon & Spa – Appointment Booking

A fully responsive Salon & Spa appointment booking web application built with **Django** (backend) and **Bootstrap 5**, HTML, and CSS (frontend).

## Features

- **User appointment booking** – No login required. Guests enter name, phone, service, date, time, and optional message.
- **Appointment status** – Pending / Approved / Rejected, managed in the admin panel.
- **Booking confirmation** – Shown immediately after submission with appointment details.
- **Admin panel** – Manage appointments (edit, approve, reject) and services (categories and individual services).
- **Double booking prevention** – Same time slot cannot be booked twice (pending/approved). Rejected slots become available again.
- **Available time slots** – Booking form shows only available times for the selected date (9:00 AM – 6:00 PM, 30‑min slots).
- **Contact page** – Salon address, phone, email, and hours.
- **Service categories** – Haircut & Styling, Facial & Skincare, Massage & Spa, Manicure & Pedicure, Hair Coloring, Bridal/Groom Packages, Beauty Treatments (seeded by default).

## Tech Stack

- **Backend:** Django 4.2+, SQLite
- **Frontend:** Bootstrap 5, HTML5, custom CSS (soft pastel / luxury theme)
- **Apps:** `pages` (home, contact), `services` (categories & services), `booking` (appointments)

## Setup

1. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations (already applied if you cloned after first run):**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser for secure admin access:**
   ```bash
   python manage.py createsuperuser
   ```
   Use this to log in at `/admin/` and manage appointments and services.

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. Open **http://127.0.0.1:8000/** in your browser.

## Project Structure

```
bookings/
├── config/             # Django project settings and URLs
├── pages/              # Home and Contact pages
├── services/           # Service categories and services (models, admin, views)
├── booking/            # Appointment booking (form, confirmation, available slots API)
├── templates/          # Base and app templates (Bootstrap 5)
├── static/css/         # Custom CSS (style.css)
├── manage.py
└── requirements.txt
```

## Admin

- **URL:** `/admin/`
- **Appointments:** List view with status badge; open any appointment to edit, approve, or reject, and add admin notes.
- **Services:** Manage categories and services (name, duration, price, active). Categories are seeded with the 7 required groups and sample services.

## Form Validation & Security

- Past dates and past times (for today) are rejected.
- Double booking is prevented in the model (`clean()`) and in the form; the available-slots API only returns free slots.
- CSRF protection and Django password validation are enabled for secure admin access.

## Customization

- **Salon name / branding:** Edit `templates/base.html` and `static/css/style.css` (e.g. `--primary-accent`, `--luxury-gold`).
- **Business hours / slot length:** Adjust `booking/views.py` in `available_slots()` (start, end, `slot_minutes`).
- **Contact details:** Update `templates/pages/contact.html` and the footer in `templates/base.html`.

---

Built with clean, commented, beginner-friendly code.
