from flask import Flask, request, send_from_directory, jsonify, abort
from datetime import datetime
import csv
import os
import json
import uuid
import sys
import threading
import webbrowser

# Optional GUI directory picker for first run configuration
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except Exception:
    tk = None
    filedialog = None

BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(__file__))

# Serve static files (html, logo, etc.) from the bundled/base directory
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

def _default_config_dir():
    # Prefer %APPDATA% on Windows, else fallback to user home
    appdata = os.environ.get('APPDATA')
    base = appdata if appdata else os.path.expanduser('~')
    cfgdir = os.path.join(base, 'TicketApp')
    os.makedirs(cfgdir, exist_ok=True)
    return cfgdir

def _config_path():
    return os.path.join(_default_config_dir(), 'config.json')

def _load_config():
    try:
        with open(_config_path(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_config(cfg: dict):
    try:
        with open(_config_path(), 'w', encoding='utf-8') as f:
            json.dump(cfg, f)
    except Exception:
        pass

def _choose_data_dir_dialog():
    if tk is None or filedialog is None:
        return None
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        selected = filedialog.askdirectory(title='Choose a folder to store ticket data (CSV & tickets)')
        root.destroy()
        return selected or None
    except Exception:
        return None

def resolve_data_dir():
    # Priority: ENV override -> saved config -> first-run dialog -> BASE_DIR/data
    env_dir = os.environ.get('TICKET_DATA_DIR')
    if env_dir and env_dir.strip():
        return env_dir
    cfg = _load_config()
    if isinstance(cfg, dict) and cfg.get('data_dir'):
        return cfg['data_dir']
    chosen = _choose_data_dir_dialog()
    if chosen:
        cfg['data_dir'] = chosen
        _save_config(cfg)
        return chosen
    # Fallback inside app directory
    return os.path.join(BASE_DIR, 'data')

# Resolve data directory (where CSV and tickets will be saved)
DATA_DIR = resolve_data_dir()

CSV_PATH = os.path.join(DATA_DIR, 'passengers.csv')
os.makedirs(DATA_DIR, exist_ok=True)
TICKETS_DIR = os.path.join(DATA_DIR, 'tickets')
os.makedirs(TICKETS_DIR, exist_ok=True)

COLUMNS = [
    'timestamp', 'name', 'id', 'seat', 'trip', 'operator',
    'departureDate', 'departureTime', 'origin', 'destination', 'price'
]

if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin') or '*'
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Vary'] = 'Origin'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def root():
    return send_from_directory(BASE_DIR, 'gui.html')

@app.route('/api/passengers', methods=['POST', 'OPTIONS'])
def add_passenger():
    if request.method == 'OPTIONS':
        return ('', 204)

    data = request.get_json(silent=True) or {}
    required_keys = ['name','id','seat','trip','operator','departureDate','departureTime','origin','destination','price']
    missing = [k for k in required_keys if not str(data.get(k, '')).strip()]
    if missing:
        return jsonify({ 'ok': False, 'error': f"Missing fields: {', '.join(missing)}" }), 400

    # Generate a unique ticket id
    ticket_id = uuid.uuid4().hex

    row = [
        datetime.utcnow().isoformat(),
        data['name'], data['id'], data['seat'], data['trip'], data['operator'],
        data['departureDate'], data['departureTime'], data['origin'], data['destination'],
        f"{float(data['price']):.2f}"
    ]

    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    # Persist JSON for lookup by QR
    ticket_doc = {
        'id': ticket_id,
        'timestamp': datetime.utcnow().isoformat(),
        'name': data['name'],
        'idNumber': data['id'],
        'seat': data['seat'],
        'trip': data['trip'],
        'operator': data['operator'],
        'departureDate': data['departureDate'],
        'departureTime': data['departureTime'],
        'origin': data['origin'],
        'destination': data['destination'],
        'price': f"{float(data['price']):.2f}"
    }
    with open(os.path.join(TICKETS_DIR, f"{ticket_id}.json"), 'w', encoding='utf-8') as jf:
        json.dump(ticket_doc, jf, ensure_ascii=False)

    return jsonify({ 'ok': True, 'id': ticket_id })

@app.get('/api/tickets/<ticket_id>')
def get_ticket(ticket_id: str):
    path = os.path.join(TICKETS_DIR, f"{ticket_id}.json")
    if not os.path.exists(path):
        abort(404)
    with open(path, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
    return jsonify(data)

if __name__ == '__main__':
    def _open_browser():
        try:
            webbrowser.open('http://127.0.0.1:3000/', new=1)
        except Exception:
            pass
    threading.Timer(0.8, _open_browser).start()
    app.run(host='127.0.0.1', port=3000)
