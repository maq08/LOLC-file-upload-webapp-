Got it 💪 — here’s your **complete README.md** in **one single Markdown block**, continuous and perfectly formatted.
You can copy this directly into your project’s `README.md` file — no cuts, no breaks.

---

````markdown
# 🏦 LOLC File Upload Web App

A Flask + SQL Server single-page web application for secure document uploads — designed with the **LOLC Microfinance Bank** theme.

---

## 📘 Overview

This project allows users to upload, manage, and submit documents safely.  
It includes **validation, database tracking, and brand-aligned UI** built using:

- **Backend:** Python (Flask) + SQLAlchemy + SQL Server  
- **Frontend:** HTML, CSS (Bootstrap 5), JavaScript (jQuery)  
- **Design:** LOLC Microfinance Bank color theme  

---

## 🎯 Key Features

| Category | Description |
|-----------|--------------|
| 🎨 **LOLC-Themed UI** | Professional design using navy blue, red, and white |
| 📂 **File Uploads** | Upload 5–10 files (each ≤ 500KB) sequentially |
| ✅ **Validation** | Checks file size, type, and total count |
| 💾 **Temporary Storage** | Uploads are first stored in `/uploads/temp/` |
| 🔒 **Final Submission** | Files moved permanently to `/uploads/permanent/` |
| ❌ **Cancel Upload** | Deletes all temporary files and DB records |
| 🔔 **Live Alerts** | Bootstrap success/error messages |
| 🧱 **Database Logging** | File metadata stored in SQL Server |
| ⚡ **Single-Page UX** | AJAX-based updates without full-page reloads |

---

## 🧠 Tech Stack

| Layer | Tools Used |
|--------|-------------|
| **Frontend** | HTML, CSS, Bootstrap 5, jQuery |
| **Backend** | Python Flask, SQLAlchemy |
| **Database** | Microsoft SQL Server (via PyODBC) |
| **Deployment** | Flask local server |
| **Design Language** | LOLC Corporate Theme |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone or Extract the Project
```bash
git clone https://github.com/anas-the-data-freestyler/LOLC-file-upload-webapp.git
cd LOLC-file-upload-webapp
````

### 2️⃣ Install Dependencies

Make sure you have **Python 3.9+** installed.

```bash
pip install -r requirements.txt
```

**requirements.txt**

```txt
Flask==3.0.3
SQLAlchemy==2.0.25
pyodbc==5.1.0
Werkzeug==3.0.4
python-dotenv==1.0.1
```

### 3️⃣ Setup SQL Server

1. Open **SQL Server Management Studio (SSMS)**
2. Run:

   ```sql
   CREATE DATABASE LOLC_Uploads;
   GO
   ```
3. In your project’s `db_connection.py`, update:

   ```python
   server = 'localhost'
   database = 'LOLC_Uploads'
   driver = 'ODBC Driver 17 for SQL Server'
   ```

### 4️⃣ Create the Table (Python-Based)

Create a new file named `create_table.py` and paste:

```python
from db_connection import get_engine
from sqlalchemy import text

engine = get_engine()

with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE UploadedFiles (
        id INT IDENTITY(1,1) PRIMARY KEY,
        upload_id VARCHAR(100),
        filename NVARCHAR(255),
        stored_name NVARCHAR(255),
        path NVARCHAR(500),
        size_bytes INT,
        status VARCHAR(20),
        created_at DATETIME DEFAULT GETDATE()
    );
    """))
print("✅ Table 'UploadedFiles' created successfully!")
```

Run:

```bash
python create_table.py
```

If successful:

```
✅ Table 'UploadedFiles' created successfully!
```

### 5️⃣ Run the Web App

```bash
python app.py
```

Then open:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🗂️ Folder Structure

```
LOLC-file-upload-webapp/
│
├── app.py
├── db_connection.py
├── create_table.py
├── requirements.txt
├── README.md
├── .env
│
├── templates/
│   └── index.html
│
├── static/
│   └── main.js
│
└── uploads/
    ├── temp/
    └── permanent/
```

---

## 🧱 Architecture Overview

| Layer                 | File                                   | Purpose                           |
| --------------------- | -------------------------------------- | --------------------------------- |
| **App Logic**         | `app.py`                               | Flask routes & upload logic       |
| **DB Connection**     | `db_connection.py`                     | SQL Server connection engine      |
| **Table Setup**       | `create_table.py`                      | Creates the `UploadedFiles` table |
| **Frontend Template** | `templates/index.html`                 | LOLC-themed HTML UI               |
| **Client Script**     | `static/main.js`                       | AJAX, validation, alerts          |
| **Storage**           | `/uploads/temp` & `/uploads/permanent` | File locations                    |

---

## 🧾 Database Schema

```sql
CREATE TABLE UploadedFiles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    upload_id VARCHAR(100),
    filename NVARCHAR(255),
    stored_name NVARCHAR(255),
    path NVARCHAR(500),
    size_bytes INT,
    status VARCHAR(20),
    created_at DATETIME DEFAULT GETDATE()
);
```

---

## 🖼️ Demo Flow (How to Present)

### 🎬 1️⃣ Introduction

> “This is a Flask + SQL Server document management app, themed after LOLC’s design system.”

### 📁 2️⃣ File Upload

* Select a valid file (<500KB) → see success alert ✅
* Try a large file → validation error ❌
* Mention the 10-file upload limit.

> “The app ensures validation and safe sequential uploads.”

### 🗃️ 3️⃣ Database Tracking

Open SSMS and run:

```sql
SELECT * FROM UploadedFiles;
```

> “Every upload is logged in SQL Server with metadata and status.”

### 🔒 4️⃣ Final Submit

Click **Final Submit** → files move from `/uploads/temp` to `/uploads/permanent`.

> “Once finalized, files are securely stored permanently.”

### ❌ 5️⃣ Cancel Upload

Upload a few files, then click **Cancel** → all temp files removed.

> “Canceling clears temp data and resets everything cleanly.”

### 🏁 6️⃣ Wrap Up

> “This app demonstrates real-world integration of Flask, SQL Server, and front-end validation with professional branding.”

---

## 💡 Demo Tips

| Tip                        | Why                                   |
| -------------------------- | ------------------------------------- |
| 🎥 Record with OBS or Loom | To showcase project professionally    |
| 📂 Show folder structure   | Demonstrates backend process visually |
| 🧾 Show database entries   | Confirms SQL integration              |
| ⏱️ Keep under 3 minutes    | Keeps it concise                      |
| ✨ End with your name       | Builds professional impression        |

---

## 👨‍💻 Author

**Muhammad Anas**
Data Consultant | Python Developer | Tableau & Excel Specialist
📍 Islamabad, Pakistan
📧 [anas.freestyler@example.com](mailto:anas.freestyler@example.com) *(replace with your actual email)*
🌐 Portfolio: [your-link-here]

---

## 🏁 Summary

This project demonstrates:

* ✅ Real-world Flask + SQL Server integration
* ✅ Secure file handling (temp + permanent storage)
* ✅ LOLC-branded responsive interface
* ✅ End-to-end functionality (upload, validate, finalize, cancel)
* ✅ Clean modular architecture ready for deployment

> “A professional, brand-consistent, and practical Python web application built for real business needs.”

```

---

✅ That’s the **entire README.md** in one Markdown block — no splits, no missing pieces — formatted perfectly for GitHub or project submission.
```
