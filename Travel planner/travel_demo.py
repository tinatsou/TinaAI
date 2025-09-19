#!/usr/bin/env python3
"""
RAG Travel Planning Demo

A command-line demo showcasing three different RAG approaches:
1. Exact keyword matching
2. BM25 (lexical ranking)
3. Embeddings (semantic similarity)

Usage: python travel_demo.py
"""

from __future__ import annotations
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
import random
import numpy as np
import pandas as pd

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=".env")
    load_dotenv(dotenv_path="../.env")
except ImportError:
    print("python-dotenv not installed. Environment variables may not be loaded.")

# Set random seeds for reproducibility
random.seed(7)
np.random.seed(7)

# Data directory
DATA_DIR = Path(__file__).parent / "data"

@dataclass
class TravelData:
    """Container for travel data"""
    activities: pd.DataFrame
    hotels: pd.DataFrame
    flights: pd.DataFrame

class RAGComparison:
    """Demonstrates different RAG approaches for travel search"""

    def __init__(self, docs: List[str]):
        self.docs = docs

    def exact_keyword_match(self, query: str, k: int = 5) -> List[Tuple[float, str]]:
        """
        Exact keyword matching: count occurrences of query tokens in each doc.
        Score = sum of term frequencies for exact tokens (case-insensitive).
        """
        q_tokens = re.findall(r"\w+", query.lower())
        scores = []
        for doc in self.docs:
            d_tokens = re.findall(r"\w+", doc.lower())
            score = sum(d_tokens.count(token) for token in q_tokens)
            if score > 0:
                scores.append((float(score), doc))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:k]

    def bm25_rank(self, query: str, k: int = 5) -> List[Tuple[float, str]]:
        """BM25 ranking with rank-bm25"""
        try:
            from rank_bm25 import BM25Okapi
        except ImportError:
            print("rank-bm25 not installed. Install with: pip install rank-bm25")
            return []

        tokenized_corpus = [re.findall(r"\w+", doc.lower()) for doc in self.docs]
        bm25 = BM25Okapi(tokenized_corpus)
        q_tokens = re.findall(r"\w+", query.lower())
        scores = bm25.get_scores(q_tokens)
        order = np.argsort(scores)[::-1][:k]
        return [(float(scores[i]), self.docs[i]) for i in order if scores[i] > 0]

    def embedding_rank(self, query: str, k: int = 5) -> List[Tuple[float, str]]:
        """
        Semantic ranking with sentence-transformers (cosine similarity).
        Falls back gracefully if package isn't installed.
        """
        try:
            from sentence_transformers import SentenceTransformer, util
        except ImportError:
            print("sentence-transformers not installed. Install with: pip install sentence-transformers")
            return []

        try:
            model = SentenceTransformer("all-MiniLM-L6-v2")
            doc_emb = model.encode(self.docs, convert_to_tensor=True, normalize_embeddings=True)
            q_emb = model.encode([query], convert_to_tensor=True, normalize_embeddings=True)[0]
            cos = (doc_emb @ q_emb).cpu().numpy()
            order = np.argsort(cos)[::-1][:k]
            return [(float(cos[i]), self.docs[i]) for i in order]
        except Exception as e:
            print(f"Error with embeddings: {e}")
            return []

class TravelPlanner:
    """RAG-based travel planner"""

    def __init__(self, travel_data: TravelData):
        self.data = travel_data

    def get_semantic_themes(self, themes: List[str], destination: str) -> List[str]:
        """Use embeddings to find semantically similar themes"""
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("all-MiniLM-L6-v2")
        except ImportError:
            print("Using exact theme matching (sentence-transformers not available)")
            return themes

        available_themes = self.data.activities.loc[
            self.data.activities['city'] == destination, 'theme'
        ].unique().tolist()

        if not available_themes:
            return themes

        close_themes = set()
        for theme in themes:
            try:
                # Find semantically similar themes
                theme_embeddings = model.encode(available_themes, normalize_embeddings=True)
                query_embedding = model.encode([theme], normalize_embeddings=True)[0]
                similarities = (theme_embeddings @ query_embedding)

                # Get top 3 most similar themes
                top_indices = np.argsort(similarities)[::-1][:3]
                top_themes = [available_themes[i] for i in top_indices if similarities[i] > 0.3]
                close_themes.update(top_themes)
                print(f"Theme '{theme}' expanded to: {top_themes}")
            except Exception as e:
                print(f"Error processing theme '{theme}': {e}")
                close_themes.add(theme)

        return list(close_themes)

    def plan_trip(self, origin: str, destination: str, start_date: str,
                  end_date: str, budget: int, themes: List[str]) -> str:
        """Generate a travel plan using RAG"""

        # Retrieve relevant data
        flights = self.data.flights[
            (self.data.flights['origin'] == origin) &
            (self.data.flights['destination'] == destination)
        ]

        hotels = self.data.hotels[self.data.hotels['city'] == destination]

        # Use semantic theme matching
        expanded_themes = self.get_semantic_themes(themes, destination)
        activities = self.data.activities[
            (self.data.activities['city'] == destination) &
            (self.data.activities['theme'].isin(expanded_themes))
        ]

        if flights.empty:
            return f"No flights found from {origin} to {destination}"
        if hotels.empty:
            return f"No hotels found in {destination}"
        if activities.empty:
            return f"No activities found in {destination} for themes: {themes}"

        # Simple planning logic (in a real app, this would use LLM)
        cheapest_flight = flights.loc[flights['price_usd'].idxmin()]
        budget_hotels = hotels[hotels['nightly_price_usd'] <= budget / 5]  # Assume 5 nights max
        budget_activities = activities[activities['cost_usd'] <= budget / 10]  # Budget constraint

        if budget_hotels.empty:
            budget_hotels = hotels.nsmallest(3, 'nightly_price_usd')
        if budget_activities.empty:
            budget_activities = activities.nsmallest(5, 'cost_usd')

        best_hotel = budget_hotels.loc[budget_hotels['review_score'].idxmax()]
        top_activities = budget_activities.nlargest(5, 'review_score') if 'review_score' in budget_activities.columns else budget_activities.head(5)

        # Create plan
        plan = f"""
# Travel Plan: {origin} → {destination}
**Dates:** {start_date} to {end_date}
**Budget:** ${budget}
**Themes:** {', '.join(themes)}

## Flight
- **{cheapest_flight['airline']}** - ${cheapest_flight['price_usd']}
- Departure: {cheapest_flight['depart_time']} → Arrival: {cheapest_flight['arrive_time']}
- On-time rate: {cheapest_flight['on_time_rate']:.1%}

## Hotel
- **{best_hotel['name']}** in {best_hotel['neighborhood']}
- ${best_hotel['nightly_price_usd']}/night - Rating: {best_hotel['review_score']:.1f}/5
- Walk Score: {best_hotel['walk_score']} - {best_hotel['notes']}

## Activities
"""

        total_activity_cost = 0
        for _, activity in top_activities.iterrows():
            plan += f"- **{activity['name']}** ({activity['theme']})\n"
            plan += f"  - Duration: {activity['duration_hours']}h - ${activity['cost_usd']}\n"
            plan += f"  - Hours: {activity['opening_hours']} - {activity['notes']}\n\n"
            total_activity_cost += activity['cost_usd']

        total_cost = cheapest_flight['price_usd'] + best_hotel['nightly_price_usd'] * 5 + total_activity_cost
        plan += f"\n## Total Estimated Cost: ${total_cost:.0f}"

        if total_cost > budget:
            plan += f" ⚠️  **OVER BUDGET by ${total_cost - budget:.0f}**"
        else:
            plan += f" ✅ **Under budget by ${budget - total_cost:.0f}**"

        return plan

def load_travel_data() -> TravelData:
    """Load travel data from CSV files"""
    try:
        activities_df = pd.read_csv(DATA_DIR / 'activities.csv')
        hotels_df = pd.read_csv(DATA_DIR / 'hotels.csv')
        flights_df = pd.read_csv(DATA_DIR / 'flights.csv')

        return TravelData(
            activities=activities_df,
            hotels=hotels_df,
            flights=flights_df
        )
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print(f"Make sure data files exist in: {DATA_DIR}")
        sys.exit(1)

def demo_rag_comparison():
    """Demonstrate the three RAG approaches"""
    print("\n" + "="*60)
    print("🔍 RAG COMPARISON DEMO")
    print("="*60)

    # Sample travel documents for comparison
    docs = [
        "San Francisco Chinatown cheap food tour",
        "Golden Gate Bridge scenic photography spot",
        "SF food trucks: affordable street eats near SOMA",
        "Jazz club in New Orleans on Frenchmen Street",
        "Seattle Pike Place Market seafood tasting",
        "Miami South Beach nightlife and bars",
        "Budget-friendly meal in San Francisco",
        "San Francisco farmers market local produce",
        "Austin BBQ and live music on Rainey Street",
        "Orlando theme parks for families"
    ]

    rag = RAGComparison(docs)
    query = "cheap food in San Francisco"

    print(f"\n🔎 Query: '{query}'\n")

    # Exact keyword matching
    print("1️⃣  EXACT KEYWORD MATCH:")
    results = rag.exact_keyword_match(query, k=3)
    for score, doc in results:
        print(f"   Score: {score:4.1f} | {doc}")

    # BM25
    print("\n2️⃣  BM25 RANKING:")
    results = rag.bm25_rank(query, k=3)
    if results:
        for score, doc in results:
            print(f"   Score: {score:8.4f} | {doc}")
    else:
        print("   (BM25 not available)")

    # Embeddings
    print("\n3️⃣  SEMANTIC SIMILARITY (Embeddings):")
    results = rag.embedding_rank(query, k=3)
    if results:
        for score, doc in results:
            print(f"   Score: {score:8.4f} | {doc}")
    else:
        print("   (Embeddings not available)")

def interactive_travel_planner():
    """Interactive travel planning demo"""
    print("\n" + "="*60)
    print("✈️  INTERACTIVE TRAVEL PLANNER")
    print("="*60)

    data = load_travel_data()
    planner = TravelPlanner(data)

    # Show available cities
    cities = sorted(data.flights['origin'].unique())
    print(f"\n📍 Available cities: {', '.join(cities)}")

    print("\n" + "-"*40)
    print("Plan your trip!")
    print("-"*40)

    try:
        origin = input("🛫 Origin city: ").strip()
        destination = input("🛬 Destination city: ").strip()
        start_date = input("📅 Start date (YYYY-MM-DD): ").strip()
        end_date = input("📅 End date (YYYY-MM-DD): ").strip()
        budget = int(input("💰 Budget ($): ").strip())
        themes_input = input("🎯 Themes (comma-separated, e.g., 'food,art,music'): ").strip()

        themes = [theme.strip() for theme in themes_input.split(',') if theme.strip()]

        print("\n" + "="*60)
        print("🗓️  GENERATING TRAVEL PLAN...")
        print("="*60)

        plan = planner.plan_trip(origin, destination, start_date, end_date, budget, themes)
        print(plan)

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def main():
    """Main demo function"""
    print("🌟 RAG TRAVEL PLANNING DEMO")
    print("Demonstrating Retrieval-Augmented Generation approaches")

    while True:
        print("\n" + "="*60)
        print("MENU:")
        print("1. 🔍 Compare RAG approaches")
        print("2. ✈️  Interactive travel planner")
        print("3. 📊 Show data statistics")
        print("4. 🚪 Exit")
        print("="*60)

        try:
            choice = input("Choose an option (1-4): ").strip()

            if choice == '1':
                demo_rag_comparison()
            elif choice == '2':
                interactive_travel_planner()
            elif choice == '3':
                show_data_stats()
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def show_data_stats():
    """Show statistics about the travel data"""
    print("\n" + "="*60)
    print("📊 TRAVEL DATA STATISTICS")
    print("="*60)

    try:
        data = load_travel_data()

        print(f"\n🏃 Activities: {len(data.activities)} total")
        print(f"   Cities: {data.activities['city'].nunique()}")
        print(f"   Themes: {', '.join(sorted(data.activities['theme'].unique()))}")

        print(f"\n🏨 Hotels: {len(data.hotels)} total")
        print(f"   Cities: {data.hotels['city'].nunique()}")
        print(f"   Price range: ${data.hotels['nightly_price_usd'].min()}-${data.hotels['nightly_price_usd'].max()}/night")

        print(f"\n✈️  Flights: {len(data.flights)} total")
        print(f"   Routes: {data.flights['origin'].nunique()} origins → {data.flights['destination'].nunique()} destinations")
        print(f"   Price range: ${data.flights['price_usd'].min()}-${data.flights['price_usd'].max()}")

    except Exception as e:
        print(f"❌ Error loading data: {e}")

if __name__ == "__main__":
    main()