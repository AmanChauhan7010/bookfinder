# 🔧 Troubleshooting Guide

Common errors and solutions for the Book Finder application.

---

## 🚀 FastAPI Issues

### Error: `Address already in use`
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Cause**: Another process is using port 8000.

**Solution**:
```bash
# Kill the existing process
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Then restart
uvicorn serving.api:app --host 0.0.0.0 --port 8000
```

---

### Error: `Search engine not ready (embeddings missing)`
```
HTTPException: 503 - Search engine not ready
```

**Cause**: Embeddings were not generated.

**Solution**:
```bash
python run_pipeline.py --embed
```

---

### Warning: `embeddings.position_ids | UNEXPECTED`

**Status**: ⚠️ **Safe to Ignore**

This is a standard transformer model notice and does not affect functionality.

---

### Browser shows `about:blank` or won't connect

**Cause**: Using `0.0.0.0` in browser instead of `localhost`.

**Solution**: Use `http://localhost:8000/docs` (not `http://0.0.0.0:8000`)

---

## 💻 Streamlit Issues

### Error: `Embeddings not loaded`

**Cause**: Missing `.pkl` embeddings file.

**Solution**:
```bash
python run_pipeline.py --embed
streamlit run serving/app.py
```

---

### Only 1-2 results showing (expected 8+)

**Cause**: Aggressive deduplication on small dataset.

**Solution**: 
1. Run pipeline with more books: `python run_pipeline.py --all --limit 100`
2. The app fetches 3x candidates internally to ensure enough unique results

---

### Search returns no results

**Cause**: Query too specific or database empty.

**Solution**:
1. Try broader queries: "science fiction" instead of "dystopian post-apocalyptic robot uprising"
2. Check DB: `sqlite3 data/books.db "SELECT count(*) FROM books;"`

---

## 📦 Installation Issues

### `ModuleNotFoundError: No module named 'sentence_transformers'`

**Solution**:
```bash
pip install -r requirements.txt
```

---

### Slow model loading (5-10 seconds)

**Status**: ✅ **Normal Behavior**

The ML model (`all-MiniLM-L6-v2`) takes time to load initially. Subsequent requests are instant.

---

## 🗄️ Database Issues

### Error: `database is locked`

**Cause**: Multiple processes accessing DB simultaneously.

**Solution**: Stop all running instances of Streamlit/API, then restart one at a time.

---

### Duplicate books appearing

**Cause**: Pipeline ran multiple times without clearing DB.

**Solution**:
```bash
# Clear and rebuild
rm data/books.db
python run_pipeline.py --all
```

---

## 📞 Getting Help

If the issue persists:
1. Check logs for detailed error messages
2. Verify all dependencies: `pip list | grep -E "streamlit|fastapi|sentence"`
3. Ensure Python version: `python --version` (Requires 3.8+)

---

**Built by**: Chauhan Aman Satpal (202518004), Devam Gandhi (202518008)
