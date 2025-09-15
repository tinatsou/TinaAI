**TinaAI – Travel‑Planning Agent Demo**

**TinaAI** is a sandbox for experimenting with retrieval‑augmented generation (RAG) and agentic tool use. The current code base centers on an end‑to‑end travel‑planning agent that combines structured data, weather APIs and large language models (LLMs) to build coherent itineraries. It grew out of Tina Tsou’s exploration of modular AI workflows and is designed to be easy to remix and extend.

**What’s inside**

**Data‑driven travel recommendations**

The travel planner ships with three simple CSV datasets: flights, hotels and activities. Each dataset has enough attributes to build a meaningful itinerary. For example, the activities.csv file lists the id, city, name, theme (e.g. sports, food, nightlife), duration, cost and other notes. flights.csv records the origin, destination, airline, price, departure/arrival time and an on‑time rate. hotels.csv contains the city, hotel name, neighbourhood, nightly price, review score and walk score. These tabular files live under Travel planner/data/ and can be easily swapped for your own data.

**Retrieval and ranking**

The Travel planner/rag.ipynb notebook demonstrates how to retrieve the most relevant activities for a query using multiple ranking strategies. It implements simple exact‑keyword matching, BM25 lexical ranking and semantic similarity via sentence transformers. These functions help narrow the large activity set down to a handful of candidates before generating an itinerary. The same notebook introduces a trip_planer function that combines the filtered flights, hotels and activities with a prompt template for an LLM. 

**Tool calling with LLMs**

Travel planner/agent.ipynb shows how to call custom functions from an LLM using OpenAI’s tool‑calling interface. Two simple Python functions are defined: get_weather, which returns a dummy current temperature for a location, and get_review, which returns placeholder reviews for a place. The notebook registers these functions in a tool schema and demonstrates how the model decides when to call them. This pattern can be extended with real API calls (e.g. to a weather service or Yelp) to enrich responses.

**Weather‑aware agent**

The most complete example is in Travel planner/complete_agent.ipynb. It defines a plan_trip method that generates a weather‑aware itinerary. The docstring explains the inputs (origin, destination, dates, budget and activity themes) and notes that it returns a formatted markdown plan. 

**Internally the agent:**

1. Fetches weather data from Open‑Meteo for the given dates, using either forecast or historical endpoints.

2. Analyses the data to determine daily conditions and classify days as suitable for outdoor or indoor activities.

3. Retrieves flights, hotels and activities filtered by the origin, destination and chosen themes.

4. Builds a detailed system prompt with planning guidelines that prioritise weather‑appropriate activities, balances cost and quality, and leaves buffer time between flights and activities.

5. Calls an LLM (via the OpenAI API) with the assembled context to generate a day‑by‑day itinerary in markdown.

This notebook is a template rather than a polished product—feel free to modify the prompt, ranking logic or data sources to suit your needs.

**Getting started**

**1. Clone the repository:**

git clone https://github.com/tinatsou/TinaAI.git
cd TinaAI/Travel\ planner

**2. Create a virtual environment and install dependencies.** The travel agent has its own requirements.txt file. Use Python 3.9+.
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt

**3. Set your API keys.** Some notebooks expect environment variables to be defined. At minimum you’ll need an OPENAI_API_KEY for LLM calls. Create a .env file or export variables like:
export OPENAI_API_KEY=sk-...  # your OpenAI key
export WEATHER_API_KEY=...    # optional if you replace dummy functions with real calls

**4. Run the notebooks.** Launch Jupyter and open any of the notebooks in Travel planner/:

rag.ipynb – play with exact, BM25 and embedding ranking on the activities dataset. Try modifying queries or experimenting with your own data.

agent.ipynb – see how an LLM can call Python functions like get_weather and get_review

complete_agent.ipynb – generate a weather‑aware travel itinerary end‑to‑end. Change the origin, destination, dates, budget and themes to see different plans.

These notebooks are self‑contained; there is no CLI yet, but you can export functions into scripts.

**Repository layout**

TinaAI/
└── Travel planner/
    ├── agent.ipynb           # demo of tool calling (weather + reviews)
    ├── rag.ipynb             # retrieval and ranking demonstrations
    ├── complete_agent.ipynb  # full weather‑aware planner
    ├── requirements.txt      # dependencies for travel‑planner notebooks
    └── data/
        ├── activities.csv    # activity catalogue (city, theme, duration, cost…):contentReference[oaicite:12]{index=12}
        ├── flights.csv       # flights (origin, destination, airline, price…):contentReference[oaicite:13]{index=13}
        └── hotels.csv        # hotels (city, neighbourhood, price, score…):contentReference[oaicite:14]{index=14}

**Contributing**

Pull requests and issues are welcome! Please open an issue to discuss significant changes, keep modules small and testable, and update docstrings or notebooks when you add features. Tests are not yet comprehensive, but adding minimal checks will help others build upon your work.

**License**

This project is released under the MIT License. See the LICENSE file for details.

**Acknowledgements**

This repo was inspired by the vibrant RAG and agent ecosystems. The travel‑planner agent is intentionally simple—it uses dummy reviews and a toy dataset—but it demonstrates how to combine retrieval, tool calls and weather analysis to craft useful outputs. Built with ❤️ by Tina Tsou.
