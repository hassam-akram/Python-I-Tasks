# Async Data Sync Dashboard

A Python project demonstrating **asyncio concurrency**, **virtual environments**, and **`.env` credential management**.


## How It Works

1. **Three mock data sources** (sales, inventory, customers) are fetched **simultaneously** using `asyncio.gather()`
2. Each source has a simulated delay (2s, 1s, 1.5s) — but because they run concurrently, total time is only ~2s
3. Results are **merged** into a combined summary and displayed as a terminal dashboard
4. **API keys** are loaded from a `.env` file stored **outside** the project folder

## Setup & Run

### 1. Create Virtual Environment
```bash
cd async_data_sync_dashboard
python -m venv venv
```

### 2. Activate the Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard
```bash
python -m src.dashboard
```

## Project Structure
```
async_data_sync_dashboard/
├── src/
│   ├── __init__.py       # Makes src a Python package
│   ├── config.py         # Loads .env credentials
│   ├── data_sources.py   # 3 async fetch functions
│   ├── merger.py         # Merges data into summary
│   └── dashboard.py      # Main entry point
├── requirements.txt
└── README.md

# .env lives at ../  (outside project folder)
```

## Key Takeaway
> Without `asyncio.gather()`, fetching from 3 sources would take **4.5 seconds** (sequential).
> With concurrency, it takes only **~2 seconds** — the time of the slowest source!
