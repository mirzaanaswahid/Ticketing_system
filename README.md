# Ticketing System

A simple ticket generation app with QR code and CSV export. Runs locally via Flask or as a packaged Windows executable.

## Features
- Enter passenger details and generate a boarding pass with QR
- Auto-save each ticket to CSV (row-by-row)
- Print-friendly layout (keeps colors and QR)
- QR links to a read-only ticket page for that passenger
- First-run prompt to choose where to save CSV/tickets

## Run from source (Windows)
1. Install Python 3.11+
2. In PowerShell:

```powershell
cd C:\MBI_project
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip flask
python .\server.py
```

Open http://127.0.0.1:3000

## Build a standalone EXE
We use PyInstaller and the provided spec file.

```powershell
cd C:\MBI_project
pip install -U pyinstaller
pyinstaller .\TicketApp.spec -y --clean
```

The EXE will be in `dist\TicketApp.exe` (one-file build). Share that single file, or zip the folder if using one-dir mode.

## Project layout
- `gui.html` – main UI
- `ticket.html` – read-only ticket page
- `server.py` – Flask server and data persistence
- `logo/` – app logo assets
- `data/` – generated CSV and ticket JSONs (created on first run)

## Support
If you encounter issues with SmartScreen, choose “More info” → “Run anyway”. If colors don’t print, enable “Print background graphics” in the print dialog.