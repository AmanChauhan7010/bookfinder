# 📚 Book Finder & Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

A powerful, modular data pipeline and semantic search engine for books. This system ingests data from public APIs, cleans and deduplicates records using professional-grade heuristics, generates vector embeddings for deep semantic understanding, and serves results via a premium Streamlit interface.

---

## ✨ Key Features

*   **🧠 Semantic Search**: Uses `sentence-transformers` (all-MiniLM-L6-v2) to understand the *meaning* behind your query. Search for "a dystopia about burning books" and find *Fahrenheit 451*.
*   **💎 High-Fidelity UI**: A fully responsive interface featuring Glassmorphism effects, modern card designs, and a "Perfect Grid" layout with intelligent image handling.
*   **🛡️ Robust Data Pipeline**: 
    *   **Advanced Deduplication**: Filtered out **~67% redundant records**, reducing the noise from 88k+ raw entries to a lean, curated set of ~29k.
    *   **Fault Tolerance**: Graceful handling of API rate limits and missing metadata.
*   **🚀 Production Ready**: Clean, modular code structure following industrial best practices for Ingestion, Transformation, Storage, and Serving.

---

## 🏗️ Architecture

The project follows a scalable micro-service-like architecture:

```
book_finder/
│
├── ingestion/          # Data harvesting (OpenLibrary API, CSVs)
├── transformation/     # Cleaning, normalization, & embedding generation
├── storage/            # SQLite DB access layer & Schema management
├── serving/            # Consumption layers (Streamlit & FastAPI)
└── run_pipeline.py     # Central CLI controller for automation
```

---

## 📊 Data Statistics (Final Audit)

After extensive deduplication and integrity checks, the system manages a robust dataset with the following health metrics:

| Metric | Value | Detail |
| :--- | :--- | :--- |
| **Total Unique Records** | **28,861** | Verified unique by (Title, Author) |
| **Database Size** | **35 MB** | Post-optimization (VACUUM) |
| **Missing Cover Images** | **10.9% (3,152)** | Handled via UI placeholders |
| **Missing ISBNs** | **<0.01% (2)** | Extremely high identifier density |
| **Missing Descriptions** | **<0.01% (11)** | High context availability for search |
| **Embedding Model** | `all-MiniLM-L6-v2` | 384-dimensional dense vectors |

### 🛠️ Data Handling Strategy
- **Collision Prevention**: A `UNIQUE` constraint is enforced on `(title, author)` at the database level.
- **Image Fallback**: Books without covers are automatically assigned a stylized CSS-based placeholder to maintain UI consistency.
- **Normalization**: Descriptions are stripped of HTML/special characters to improve the accuracy of the semantic embedding engine.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Docker** (Optional, for deployment)

### Installation
1.  **Clone the Repository**
    ```bash
    git clone <your-repo-link>
    cd book_finder
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🏃‍♂️ Usage

### 1. Build the Database (The Pipeline)
```bash
# Run the full pipeline (Ingest -> Transform -> Embed -> Store)
python run_pipeline.py --all --limit 50
```

### 2. Run the User Interface
```bash
streamlit run serving/app.py
```

### 3. Deployment
See the [**README_DEPLOY.md**](./README_DEPLOY.md) for full instructions on launching to Hugging Face or Render.

---

## � Documentation & Playbook
- [**TROUBLESHOOTING.md**](./TROUBLESHOOTING.md): Common fixes for environment issues.

---

## 👥 Contributors
Built by the Data Engineering Team for the DAU Project.
- **Chauhan Aman Satpal** 
- **Devam Gandhi**

---
*DAU Project - Big Data Engineering*
