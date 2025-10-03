const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Storage locations
const DATA_DIR = path.join(__dirname, 'data');
const CSV_PATH = path.join(DATA_DIR, 'passengers.csv');

// Ensure data directory exists
fs.mkdirSync(DATA_DIR, { recursive: true });

// CSV columns and header
const COLUMNS = [
  'timestamp',
  'name',
  'id',
  'seat',
  'trip',
  'operator',
  'departureDate',
  'departureTime',
  'origin',
  'destination',
  'price'
];

if (!fs.existsSync(CSV_PATH)) {
  fs.writeFileSync(CSV_PATH, COLUMNS.join(',') + '\n', 'utf8');
}

// Basic CORS to allow requests from file:// and http://localhost origins
app.use((req, res, next) => {
  const origin = req.headers.origin || '*';
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

app.use(express.json({ limit: '1mb' }));

// Serve static files so you can open gui.html via http://localhost:3000/
app.use(express.static(__dirname));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'gui.html'));
});

function escapeCSV(value) {
  if (value === null || value === undefined) return '';
  const str = String(value);
  if (/[",\n]/.test(str)) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

app.post('/api/passengers', (req, res) => {
  try {
    const {
      name,
      id,
      seat,
      trip,
      operator,
      departureDate,
      departureTime,
      origin,
      destination,
      price
    } = req.body || {};

    // Minimal validation
    const required = { name, id, seat, trip, operator, departureDate, departureTime, origin, destination, price };
    const missing = Object.entries(required)
      .filter(([, v]) => v === undefined || v === null || String(v).trim() === '')
      .map(([k]) => k);
    if (missing.length) {
      return res.status(400).json({ ok: false, error: `Missing fields: ${missing.join(', ')}` });
    }

    const nowIso = new Date().toISOString();
    const row = [
      nowIso,
      name,
      id,
      seat,
      trip,
      operator,
      departureDate,
      departureTime,
      origin,
      destination,
      Number(price).toFixed(2)
    ]
      .map(escapeCSV)
      .join(',') + '\n';

    fs.appendFileSync(CSV_PATH, row, 'utf8');
    return res.json({ ok: true });
  } catch (err) {
    console.error('Failed to append CSV:', err);
    return res.status(500).json({ ok: false, error: 'Failed to save passenger' });
  }
});

app.listen(PORT, () => {
  console.log(`Ticket CSV server running at http://localhost:${PORT}`);
  console.log(`CSV file: ${CSV_PATH}`);
});
