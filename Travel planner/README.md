# RAG Travel Planning Demo

A demonstration of **Retrieval-Augmented Generation (RAG)** techniques for travel planning, showcasing three different approaches to document retrieval and ranking.

## 🌟 Features

- **Three RAG Approaches Comparison**:
  1. **Exact Keyword Matching**: Simple term frequency scoring
  2. **BM25**: State-of-the-art lexical ranking algorithm
  3. **Semantic Embeddings**: Neural embedding-based similarity search

- **Interactive Travel Planner**: Plan trips with budget constraints and theme preferences
- **Real Travel Data**: Activities, hotels, and flights across 15 cities
- **Command-Line Interface**: Easy-to-use CLI for demonstrations

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install pandas numpy matplotlib rank-bm25 python-dotenv
```

### 2. Run the Demo

**Quick Non-Interactive Demo:**
```bash
python demo_runner.py
```

**Full Interactive Demo:**
```bash
python travel_demo.py
```

**Jupyter Notebook (Original):**
```bash
jupyter notebook rag.ipynb
```

## 📊 What You'll See

### RAG Approach Comparison
The demo compares how different retrieval methods rank documents for the query "cheap food in San Francisco":

- **Exact Keyword**: Counts exact word matches
- **BM25**: Uses inverse document frequency and term saturation
- **Embeddings**: Finds semantically similar content (requires `sentence-transformers`)

### Travel Planning
Generate complete travel plans including:
- Flight recommendations
- Hotel suggestions
- Activity recommendations based on themes
- Budget analysis

## 🛠 Optional: Enhanced Semantic Search

For the full semantic search experience, install sentence-transformers:

```bash
pip install sentence-transformers
```

This enables the embedding-based RAG approach that can find semantically similar themes (e.g., "art" → "arts", "museums", "galleries").

## 📁 Project Structure

```
RAG/
├── data/
│   ├── activities.csv    # 225 activities across 15 cities
│   ├── hotels.csv        # 150 hotels with ratings and prices
│   └── flights.csv       # 210 flight routes with pricing
├── travel_demo.py        # Full interactive demo
├── demo_runner.py        # Quick non-interactive demo
├── rag.ipynb            # Original Jupyter notebook
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎯 Demo Scenarios

### Scenario 1: RAG Comparison
- Compares three retrieval approaches on sample travel documents
- Shows how different algorithms rank the same content
- Demonstrates strengths and weaknesses of each method

### Scenario 2: Travel Planning
- Interactive trip planning with real data
- Budget constraints and theme preferences
- Semantic theme expansion (with embeddings)

## 🔧 Technical Details

### RAG Approaches Implemented

1. **Exact Keyword Matching**
   - Simple but effective for exact term matches
   - Fast and lightweight
   - Limited by vocabulary gaps

2. **BM25 (Best Matching 25)**
   - Industry standard for lexical search
   - Handles term frequency and document length normalization
   - Used by search engines like Elasticsearch

3. **Semantic Embeddings**
   - Uses transformer models for semantic understanding
   - Can find conceptually related content
   - Requires more computational resources

### Data Schema

**Activities**: id, city, name, theme, duration_hours, cost_usd, opening_hours, notes
**Hotels**: id, city, name, neighborhood, nightly_price_usd, review_score, walk_score, notes
**Flights**: id, origin, destination, airline, price_usd, depart_time, arrive_time, on_time_rate

## 🎮 Interactive Commands

When running `python travel_demo.py`:

1. **🔍 Compare RAG approaches** - See all three methods in action
2. **✈️ Interactive travel planner** - Plan a custom trip
3. **📊 Show data statistics** - Explore the dataset
4. **🚪 Exit** - Quit the demo

## 🌍 Available Cities

The demo includes travel data for: Austin, Boston, Chicago, Denver, Las Vegas, Los Angeles, Miami, New Orleans, New York City, Orlando, Portland, San Diego, San Francisco, Seattle, Washington DC.

## 📝 Example Usage

```bash
$ python demo_runner.py

🔎 Query: 'cheap food in San Francisco'

1️⃣  EXACT KEYWORD MATCH:
   Score:  4.0 | San Francisco Chinatown cheap food tour
   Score:  3.0 | Budget-friendly meal in San Francisco
   Score:  2.0 | San Francisco farmers market local produce

2️⃣  BM25 RANKING:
   Score:   4.7586 | San Francisco Chinatown cheap food tour
   Score:   2.8466 | Budget-friendly meal in San Francisco
   Score:   1.5789 | San Francisco farmers market local produce

✈️  Planning trip from Austin to Boston...
# Travel Plan: Austin → Boston
**Budget:** $1500
**Total Cost:** $1154 ✅ Under budget by $346
```

## 🔮 Next Steps

- Integrate with OpenAI API for LLM-generated plans
- Add more sophisticated ranking algorithms
- Implement hybrid retrieval (lexical + semantic)
- Add real-time pricing and availability
- Create web interface

---

**Built with**: Python, pandas, rank-bm25, sentence-transformers
**Demo Purpose**: Educational demonstration of RAG techniques in travel planning