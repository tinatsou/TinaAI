#!/usr/bin/env python3
"""
Quick Demo Runner for RAG Travel Planning

This script runs a non-interactive demonstration of the RAG travel planning system,
showcasing all three approaches and a sample travel plan.
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import from travel_demo
sys.path.insert(0, str(Path(__file__).parent))

from travel_demo import RAGComparison, TravelPlanner, load_travel_data

def main():
    print("🌟" * 30)
    print("RAG TRAVEL PLANNING DEMO")
    print("🌟" * 30)

    print("\n📊 LOADING TRAVEL DATA...")
    try:
        data = load_travel_data()
        print(f"✅ Loaded: {len(data.activities)} activities, {len(data.hotels)} hotels, {len(data.flights)} flights")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    print("\n" + "="*60)
    print("🔍 DEMONSTRATING RAG APPROACHES")
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

    # Demonstrate each approach
    print("1️⃣  EXACT KEYWORD MATCH:")
    results = rag.exact_keyword_match(query, k=3)
    for score, doc in results:
        print(f"   Score: {score:4.1f} | {doc}")

    print("\n2️⃣  BM25 RANKING:")
    results = rag.bm25_rank(query, k=3)
    if results:
        for score, doc in results:
            print(f"   Score: {score:8.4f} | {doc}")
    else:
        print("   (BM25 not available)")

    print("\n3️⃣  SEMANTIC SIMILARITY (Embeddings):")
    results = rag.embedding_rank(query, k=3)
    if results:
        for score, doc in results:
            print(f"   Score: {score:8.4f} | {doc}")
    else:
        print("   (Embeddings not available - install sentence-transformers)")

    print("\n" + "="*60)
    print("✈️  SAMPLE TRAVEL PLAN")
    print("="*60)

    # Create a sample travel plan
    planner = TravelPlanner(data)

    # Check available cities
    available_cities = sorted(data.flights['origin'].unique())
    print(f"\n📍 Available cities: {', '.join(available_cities[:5])}...")

    if len(available_cities) >= 2:
        origin = available_cities[0]
        destination = available_cities[1] if available_cities[1] != origin else available_cities[2]

        print(f"\n🗓️  Planning trip from {origin} to {destination}...")

        plan = planner.plan_trip(
            origin=origin,
            destination=destination,
            start_date="2025-12-01",
            end_date="2025-12-05",
            budget=1500,
            themes=["food", "arts"]
        )

        # Print the plan with some formatting
        for line in plan.split('\n'):
            if line.strip():
                print(line)
    else:
        print("❌ Insufficient data for travel planning demo")

    print("\n" + "="*60)
    print("🎉 DEMO COMPLETE!")
    print("="*60)
    print("To run the interactive version: python travel_demo.py")
    print("To explore the Jupyter notebook: jupyter notebook rag.ipynb")

if __name__ == "__main__":
    main()