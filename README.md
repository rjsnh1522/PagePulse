# 📊 Self-Hosted Analytics Tool

A **privacy-friendly, self-hosted analytics solution** to track user activity across websites.  
Built with **FastAPI backend**, **JavaScript tracker**, and an **Admin Panel** using SQLAdmin.

---

## 🚀 Features

- 🟢 Lightweight JavaScript tracker (`tracker.js`) – easy to embed.
- 🟢 Tracks:
  - Unique Visitor ID (persistent via LocalStorage)
  - Visitor Session ID (per page load/session)
  - Scroll depth (how much user scrolled)
  - Time spent on each page
  - IP-based geolocation (country, city, region, latitude, longitude, ISP)
- 🟢 IP lookup with fallback between:
  - `ipapi.co`  
  - `ipinfo.io`
- 🟢 Admin Panel (SQLAdmin):
  - Manage domains/websites.
  - View visitors, sessions, and analytics data.
- 🟢 PostgreSQL with SQLAlchemy ORM & Alembic migrations.
- 🟢 Scalable architecture for multi-tenant (SaaS-ready).

---

## 🏗️ Architecture

- **Backend:** FastAPI  
- **Database:** PostgreSQL (SQLAlchemy ORM)  
- **Admin Panel:** SQLAdmin (FastAPI integrated)  
- **Frontend Tracker:** Lightweight JavaScript snippet (`tracker.js`)

---

## ⚡ Getting Started

### 1️⃣ Clone the Repo:
```bash
git clone https://your-repo-url.git
cd analytics-tool
```
### 2️⃣ Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4️⃣ Run Alembic Migrations:
```bash
    DATABASE_URL=postgresql+psycopg2://username:password@localhost/dbname
```
5️⃣ Start the FastAPI Server:

```bash
uvicorn main:app --reload
```


💻 Embedding the Tracker JS
After adding your domain through the Admin Panel, place this snippet inside your website’s <head>:

```html
<script>
    window.trackerDomainId = "YOUR_DOMAIN_ID";  <!-- Replace with your actual domain ID -->
</script>
<script src="https://your-backend-url.com/static/tracker.js"></script>

```


