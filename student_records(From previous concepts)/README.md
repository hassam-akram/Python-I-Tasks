

## Setup Instructions

### 1. Create Virtual Environment
```bash
cd \student_records
python -m venv venv
```

### 2. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```

### 5. Deactivate When Done
```bash
deactivate
```

## Features

| Feature | Concepts Used |
|---------|---------------|
| Add Student | OOP, generators, decorators, validation, exceptions |
| View All | Batch generators, polymorphism, formatting |
| Search | List comprehension, string methods |
| Update | **kwargs, property setters, decorators |
| Delete | Stacked decorators (@require_auth + @log_action) |
| Statistics | Functional paradigm — map, filter, reduce, lambda |
| Export (Threaded) | threading module, Lock, join |
| Export (Multiprocess) | multiprocessing.Pool, GIL bypass |
| Export (Async) | asyncio, async/await, gather |
| Data Persistence | JSON file I/O, CSV export |

## Admin Password

The admin password is stored in `.env` file. Default: `admin123`

## Project Structure

```
student_records/
├── .env                    # Secrets (gitignored)
├── .gitignore
├── requirements.txt
├── README.md
├── main.py                 # Entry point
├── config/                 # Configuration
├── models/                 # Data models (OOP)
├── services/               # Business logic
├── utils/                  # Helpers (decorators, generators, validators)
└── data/                   # Auto-generated data files
```
