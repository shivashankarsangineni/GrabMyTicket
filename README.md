<img src="frontend\src\img\GrabMyTicket.png" width="150" alt="GrabTickets Logo"/>

# GrabTickets (Smart Ticketing Web Application)

## Contents
* [Overview](#overview)
* [Key Features](#key-features)
  * [User Registration & Login](#user-registration--login)
  * [Browse Events & Purchase Tickets](#browse-events--purchase-tickets)
  * [User Dashboard](#user-dashboard)
  * [QR Code Ticket System](#qr-code-ticket-system)
  * [Live Ticket Scanning](#live-ticket-scanning)
  * [Secure Ticket Verification](#secure-ticket-verification)
* [Getting Started](#getting-started)
  * [Docker Setup](#docker-setup)
  * [Manual Setup](#manual-setup)

---

## Overview
GrabTickets is a full-stack web application designed for secure and efficient event ticketing.  
Users can explore events, purchase tickets, and receive unique QR codes for entry.  
Event organizers can scan QR codes on-site to instantly verify authenticity.  
The system uses **digital signatures** to prevent tampering and secure ticket data.

**Tech Stack:**
- **Backend:** Flask (Python)
- **Frontend:** React (JavaScript)
- **Database:** MySQL
- **Web Server:** Nginx

---

## Key Features

### User Registration & Login
- Create accounts and sign in securely.
- All new accounts default to the “customer” role.
- Admin and manager accounts are created from the server.

<img src=".screenshots/register.png" width="150"/> <img src=".screenshots/login.png" width="150"/>

---

### Browse Events & Purchase Tickets
- View upcoming events and detailed descriptions.
- Choose ticket type (Standard, VIP, Deluxe) and quantity.
- Easy, responsive checkout process.

<img src=".screenshots/home_user.png" width="150"/> <img src=".screenshots/event_details.png" width="150"/> <img src=".screenshots/buy_ticket.png" width="150"/>

---

### User Dashboard
- Access personal info and booking history.
- View all purchased tickets in one place.

<img src=".screenshots/account.png" width="150"/>

---

### QR Code Ticket System
- Generate unique QR codes for every ticket.
- Anti-fraud measures:
  - Animated logo overlay
  - Fireworks animation when tapped/clicked
- Backend validation:
  - Session-based unique QR codes
  - Digital signature for tamper-proof tickets
  - One-time use QR codes

<img src=".screenshots/qr_code.png" width="150"/>

---

### Live Ticket Scanning
- Admin dashboard for live QR scanning at events.

<img src=".screenshots/home_management.png" width="150"/> <img src=".screenshots/scanner.png" width="150"/>

---

### Secure Ticket Verification
- Real-time ticket validation.
- Shows ticket type if valid.
- Displays error messages for:
  - Expired tickets
  - Wrong event
  - Duplicate/used tickets
  - Modified QR codes

<img src=".screenshots/ticket_valid.png" width="150"/> <img src=".screenshots/ticket_invalid.png" width="150"/> <img src=".screenshots/ticket_invalid_used.png" width="150"/> <img src=".screenshots/ticket_invalid_outdated.png" width="150"/> <img src=".screenshots/ticket_invalid_wrong_event.png" width="150"/>

---

## Getting Started

### Docker Setup
**Requirements:**
- Docker installed on your system.

**Steps:**
1. In the root folder (where `docker-compose.yml` is located), create a `.env` file:
```
# Flask
SECRET_KEY=<YOUR_SECRET_KEY>
JWT_SECRET_KEY=<YOUR_JWT_KEY>

# MySQL
MYSQL_HOST=db
MYSQL_DATABASE=<DB_NAME>
MYSQL_USER=<USER>
MYSQL_PASSWORD=<PASSWORD>

# Host Address
HOST=<YOUR_IP>
```

2. Generate a self-signed SSL certificate:
```bash
mkdir -p nginx/certs
cd nginx/certs
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

3. Run the application:
```bash
docker-compose up
```

4. (Optional) Add sample data:
```bash
docker exec grabtickets-flask-1 python sample_data.py
```

**Test Accounts:**
- User: `test@test.com` / `test1234`
- Admin: `admin@test.com` / `test1234`

Access via:
```
https://<YOUR_IP>
```

---

### Manual Setup
Run Flask and React separately for development.  
See:
- [Flask README](flask-server/README.md)
- [React README](frontend/README.md)
