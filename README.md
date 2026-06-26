# CodeSearch — Coding Problem Search Engine

Search LeetCode problems by keyword using TF-IDF ranking.

Live demo: https://search-question.onrender.com

## Features
- TF-IDF keyword search across 2000+ LeetCode problems
- Platform filter (LeetCode, Codeforces, CodeChef)
- Recent searches saved in browser
- Loading spinner and empty states
- Mobile responsive

## Tech Stack
| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | Flask + Flask-WTF |
| Algorithm | TF-IDF (built from scratch) |
| Frontend | HTML, CSS, Vanilla JS |
| Deployment | Render (gunicorn) |

## Running Locally
\```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python query.py
\```

Open http://localhost:5000