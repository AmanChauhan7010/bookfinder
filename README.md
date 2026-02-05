# 📚 Book Finder & Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

A powerful, modular data pipeline and semantic search engine for books. This system ingests data from public APIs, cleans and deduplicates records, generates vector embeddings for semantic understanding, and serves results via a premium, "industry-standard" user interface.

## ✨ Key Features

*   **🧠 Semantic Search**: Uses `sentence-transformers` to understand the *meaning* behind your query, not just keyword matching. Search for "a dystopia about burning books" and find *Fahrenheit 451*.
*   **💎 Premium UI**: A fully responsive Streamlit interface featuring:
    *   Glassmorphism effects & Modern Cards.
    *   Dark mode aesthetic with neon accents.
    *   "Perfect Grid" layout with smart image cropping.
*   **🛡️ Robust Pipeline**:
    *   **Deduplication**: Intelligent filtering of duplicate book records based on normalized title/author pairs.
    *   **Fault Tolerance**: Graceful handling of API rate limits and missing data.
*   **🚀 Production Ready**: Clean, modular code structure separating Ingestion, Transformation, Storage, and Serving layers.

## 🏗️ Architecture

The project follows a scalable micro-service-like architecture:

```
book_finder/
│
├── ingestion/          # Data harvesting (OpenLibrary API, CSVs)
├── transformation/     # Cleaning, normalization, & embedding generation
├── storage/            # SQLite DB access layer
├── serving/            # Consumption layers
│   ├── api.py          # FastAPI backend
│   └── app.py          # Streamlit frontend
└── run_pipeline.py     # Central CLI controller
```

## 📊 Data Statistics

The system currently manages a robust dataset of over 88,000 books.

| Metric | Value | details |
| :--- | :--- | :--- |
| **Total Books** | **88,232** | Unique records after deduplication |
| **Database Size** | **101 MB** | SQLite file with indices |
| **Embedding Model** | `all-MiniLM-L6-v2` | 384-dimensional dense vectors |
| **Data Quality** | **Missing Covers:** 9,720 (11%)<br>**Missing Descriptions:** 45 (<0.1%) | *Handled via UI placeholders* |
| **Primary Sources** | OpenLibrary API | Subjects: Sci-Fi, Thriller, History, etc. |

## 🚀 Getting Started

### Prerequisites

*   **Python 3.8+**
*   **Pip** (Python Package Installer)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/book-finder.git
    cd book_finder
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

### 1. Build the Database (The Pipeline)
Before running the app, you need to populate the database and generate embeddings.

```bash
# Run the full pipeline (Ingest -> Transform -> Embed -> Store)
python run_pipeline.py --all --limit 50
```

*Arguments:*
*   `--ingest`: Fetch fresh data from OpenLibrary.
*   `--transform`: Clean and normalize data.
*   `--embed`: Generate vector embeddings (Crucial for search).
*   `--store`: Save to SQLite.
*   `--limit [N]`: Number of books to fetch per genre.

### 2. Run the User Interface
Launch the modern Streamlit web application:

```bash
streamlit run serving/app.py
```

*   Opens automatically in your browser at `http://localhost:8501`.
*   **Features**: Interactive sliders, detailed book views, and history navigation.

### 3. Run the API (Backend)
For programmatic access or integration:

```bash
uvicorn serving.api:app --host 0.0.0.0 --port 8000
```

*   **Docs**: Visit `http://localhost:8000/docs` for interactive Swagger UI.
*   **Endpoint**: `GET /books/recent`

## 🔧 Troubleshooting

| Problem | Solution |
| :--- | :--- |
| **"Embeddings not loaded" error** | You skipped the embedding step. Run `python run_pipeline.py --embed` to generate vectors. |
| **No images showing** | Some OpenLibrary records lack covers. The UI handles this with a stylized placeholder. |
| **Duplicates in search** | The pipeline now auto-deduplicates. Re-run `python run_pipeline.py --all` to clean your DB. |

## 🛠 Tech Stack

*   **Ingestion**: `requests`, OpenLibrary API
*   **Processing**: `pandas`, `numpy`
*   **AI/ML**: `sentence-transformers`, `scikit-learn`
*   **Frontend**: `streamlit` (Custom CSS)
*   **Backend**: `fastapi`, `uvicorn`, `sqlite3`

## 👥 Contributors

Built by the Data Engineering Team:

*   **Chauhan Aman Satpal** (SID: 202518004)
*   **Devam Gandhi** (SID: 202518008)

---

*DAU Project - Big Data Engineering*
