# LOLC File Upload Web App

Single-page Flask app for 5-10 doc uploads (≤500KB), sequential, with edit/remove/submit/cancel. SQL Server backend.

## Setup
1. `pip install -r requirements.txt`
2. Edit `config.py` for SQL Server.
3. `python app.py`
4. http://127.0.0.1:5000/

## Features
- One-by-one AJAX uploads.
- DB tracks status ('temp' → 'saved').
- Cancel: Nukes temps.

## Changes
- v1.0: Core upload/edit.
