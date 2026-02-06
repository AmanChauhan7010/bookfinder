import torch
try:
    torch.classes.__path__ = []
except AttributeError:
    pass

import streamlit as st
# ... rest of your imports

import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to sys.path to resolve 'storage' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from storage.db import get_recent_books, search_books, get_books_by_ids
from transformation.embedder import load_model, load_embeddings, generate_embeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(page_title="Book Finder", page_icon="📚", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background */
    .stApp {
        background-color: #0F1116;
    }

    /* Hero Section Styling */
    .hero-container {
        text-align: center;
        padding: 4rem 0;
        max-width: 800px;
        margin: 0 auto;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #A8C0FF, #3F2B96);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 2rem;
    }

    /* Card Styling */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        transition: transform 0.2s, box-shadow 0.2s;
        overflow: hidden;
    }
    div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        border-color: #58A6FF;
    }

    /* Typography in Cards */
    h4 {
        color: #F0F6FC !important;
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    p, span, div {
        color: #8B949E;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(90deg, #6e40c9 0%, #8957e5 100%); /* Purple Brand Gradient */
        color: white !important;
        border: none;
        border-radius: 20px; /* Pill shape */
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #8957e5 0%, #6e40c9 100%);
        box-shadow: 0 6px 12px rgba(137, 87, 229, 0.4); /* Purple glow */
        color: white !important;
        transform: translateY(-2px);
    }
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* Input Styling */
    .stTextInput input {
        background-color: #0D1117;
        border: 1px solid #30363D;
        color: white;
        border-radius: 10px;
        padding: 1rem;
    }
    .stTextInput input:focus {
        border-color: #58A6FF;
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.3);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# sidebar hidden by default to keep it clean, but kept enabled code-wise
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    limit = st.slider("Results Limit", 4, 30, 8, step=2)
    st.markdown("---")
    st.info("Built with Python & Streamlit")

# --- RESOURCE LOADING ---
@st.cache_resource
@st.cache_resource
def load_search_resources():
    try:
        model = load_model()
        embeddings_data = load_embeddings()
        return model, embeddings_data
    except Exception as e:
        # This will show you the real error on the webpage
        st.error(f"Error loading resources: {e}")
        return None, None

model, embeddings_data = load_search_resources()

def semantic_search(query_text, top_k=5):
    if not embeddings_data or not model: return [], []
    query_embedding = model.encode([query_text])
    stored_embeddings = embeddings_data['embeddings']
    scores = cosine_similarity(query_embedding, stored_embeddings)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    ids = np.array(embeddings_data['ids'])[top_indices]
    return ids.tolist(), scores[top_indices]

# --- STATE MANAGEMENT ---
if 'view' not in st.session_state:
    st.session_state.view = 'list'
if 'selected_book' not in st.session_state:
    st.session_state.selected_book = None
if 'query' not in st.session_state:
    st.session_state.query = ""

def view_book_details(book):
    st.session_state.selected_book = book
    st.session_state.view = 'detail'

def go_back():
    st.session_state.view = 'list'
    st.session_state.selected_book = None
    # Ensure query persists
    
def update_query():
    st.session_state.query = st.session_state.search_input

# --- VIEWS ---

if st.session_state.view == 'detail':
    # --- DETAIL PAGE ---
    book = st.session_state.selected_book
    if book:
        st.button("← Back to Search", on_click=go_back)
        
        st.markdown(f"## {book.get('title')}")
        
        col_img, col_info = st.columns([1, 2])
        with col_img:
            if book.get('cover_image'):
                 st.image(book['cover_image'], use_container_width=True)
            else:
                 st.markdown(f"<div style='height:400px; background-color:#21262d; display:flex; align-items:center; justify-content:center; border-radius:12px; font-size:80px;'>📕</div>", unsafe_allow_html=True)

        with col_info:
            st.markdown(f"**Author:** {book.get('author') or 'Unknown'}")
            st.markdown(f"**Published:** {book.get('publish_year')} | **ISBN:** {book.get('isbn') or 'N/A'}")
            st.markdown(f"**Genre:** {book.get('genre')}")
            
            st.markdown("#### Abstract")
            st.write(book.get('description') or "No description available.")
            
            st.markdown("---")
            st.caption(f"Source ID: {book.get('id')}")

else:
    # --- LIST PAGE (HERO & SEARCH) ---
    
    # Hero Section
    if not st.session_state.query:
        st.markdown("""
            <div class="hero-container">
                <div class="hero-title">Discover Your Next Read</div>
                <div class="hero-subtitle">Semantic search powered by AI. Describe the vibe, plot, or character you're looking for.</div>
            </div>
        """, unsafe_allow_html=True)

    # Card Alignment CSS
    st.markdown("""
    <style>
        .stButton button {
            width: 100%;
        }
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            height: 480px; /* Increased Fixed card height */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding-bottom: 10px;
        }
        .title-text {
            display: -webkit-box;
            -webkit-line-clamp: 2; /* Limit to 2 lines */
            -webkit-box-orient: vertical;
            white-space: normal; /* Allow wrapping */
            overflow: hidden;
            text-overflow: ellipsis;
            font-weight: bold;
            font-size: 1.15rem;
            color: #F0F6FC;
            margin-top: 5px;
            line-height: 1.3;
            height: 3em; /* Enforce height for alignment */
        }
        .author-text {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #8B949E;
            font-size: 0.95rem;
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Search Bar (Centered layout sort of handled by Streamlit's flow)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        query = st.text_input(
            "Search for a book", 
            placeholder="e.g., 'A mystery novel set in Victorian London'...", 
            label_visibility="collapsed",
            key="search_input",
            value=st.session_state.query,
            on_change=update_query
        )
    
    st.write("") # Spacer

    if st.session_state.query:
        query = st.session_state.query
        
        if embeddings_data and model:
            with st.spinner("Analyzing semantic meaning..."):
                # Fetch 3x candidates to ensure enough unique results after dedup
                ids, scores = semantic_search(query, top_k=limit * 3)
            
            if ids:
                st.markdown(f"##### Best Matches")
                # Books Fetch
                books = get_books_by_ids(ids)
                book_map = {b['id']: b for b in books}
                ordered_books = [book_map[id] for id in ids if id in book_map]

                # De-dup logic
                seen_isbns = set()
                seen_titles = set()
                unique_books = []
                unique_scores = []

                for b, s in zip(ordered_books, scores):
                    if len(unique_books) >= limit: break # Stop once we have enough
                    
                    isbn = b.get('isbn')
                    t = (b.get('title') or "").lower().strip()
                    a = (b.get('author') or "").lower().strip()
                    key = (t,a)
                    if isbn and isbn in seen_isbns: continue
                    if key in seen_titles: continue
                    if isbn: seen_isbns.add(isbn)
                    if t: seen_titles.add(key)
                    unique_books.append(b)
                    unique_scores.append(s)

                # Grid Render
                cols = st.columns(4) # 4 columns for wider consumer look
                for i, (book, score) in enumerate(zip(unique_books, unique_scores)):
                    with cols[i % 4]:
                        with st.container(border=True): # Uses card css
                            # Image
                            if book.get('cover_image'):
                                try:
                                    st.markdown(f"""
                                    <div style="height:280px; width:100%; overflow:hidden; border-radius:8px; margin-bottom:10px;">
                                        <img src="{book['cover_image']}" style="width:100%; height:100%; object-fit:cover; object-position:top;">
                                    </div>
                                    """, unsafe_allow_html=True)
                                except:
                                    st.markdown("<div style='height:280px; background:#21262d; border-radius:8px; margin-bottom:10px;'></div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div style='height:280px; background-color:#21262d; color:#8b949e; display:flex; align-items:center; justify-content:center; border-radius:8px; margin-bottom:10px;'>{book.get('title')[:15]}...</div>", unsafe_allow_html=True)
                            
                            # Content Container for alignment
                            st.markdown(f"""
                                <div style="flex-grow:1;">
                                    <div class="title-text" title="{book.get('title')}">{book.get('title')}</div>
                                    <div class="author-text">{book.get('author') or 'Unknown'}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            match_color = "#238636" if score > 0.5 else "#d29922"
                            st.markdown(f"<span style='color:{match_color}; font-size:0.8rem'>● Match {score:.0%}</span>", unsafe_allow_html=True)
                            
                            st.button("View Details", key=f"btn_{book['id']}", on_click=view_book_details, args=(book,))
            else:
                st.warning("No matches found.")
        else:
             st.error("Embeddings not loaded.")
