## TinaAI – AI  Header

**TinaAI** is a sandbox for experimenting with different AI workflows, including retrieval‑augmented generation (RAG), agentic tool use, interactive storytelling and simple productivity tools. Each sub‑directory in this repository contains a self‑contained demo that showcases how large language models can be combined with data and functions to produce useful outputs.

## Projects

* **Travel planner** – An end‑to‑end travel‑planning agent that combines structured data, weather APIs and an LLM to build coherent, weather‑aware itineraries. See [Travel planner/](Travel%20planner/) for notebooks and details.
* **ChatGPT-based storytelling** – A choose‑your‑own‑adventure‑style story project built with ChatGPT. Readers follow a team of heroes through a fantasy world and make decisions that lead to different story paths. See [chatgpt_storytelling/](chatgpt_storytelling/) for the interactive story and write‑up.
* **Personal expense tracker** – A simple command‑line tool to log daily expenses, set a monthly budget and track spending against it. Expenses are persisted to a CSV file. See [expense_tracker/personal_expense_tracker.py](expense_tracker/personal_expense_tracker.py) for details and usage.

---

## Travel planner

This was the original demo in the repository and remains the most fully fledged example. It shows how to build a RAG‑based agent that retrieves relevant activities, flights and hotels and calls external functions (e.g. weather) when generating a trip plan.

### Data‑driven travel recommendations

The travel planner ships with three simple CSV datasets: **flights**, **hotels** and **activities**. Each dataset has enough attributes to build a meaningful itinerary. For example, the `activities.csv` file lists the id, city, name, theme (e.g. outdoors, food, nightlife), duration, cost and other notes. `flights.csv` records the origin, destination, airline, price, departure/arrival time and an approximate distance. `hotels.csv` contains the city, hotel name, neighbourhood, nightly price, review score and walk score. These tabular files live under `Travel planner/data/` and can be easily swapped for your own data.

### Retrieval and ranking

The `Travel planner/rag.ipynb` notebook demonstrates how to retrieve the most relevant activities for a query using multiple ranking strategies. It implements simple exact‑keyword matching, BM25 lexical ranking and semantic similarity via sentence transformers. These functions help narrow the large activity set down to a handful of candidates before generating an itinerary. The same notebook introduces a `trip_planner` function that combines the filtered flights, hotels and activities with a prompt template for an LLM.

### Tool calling with large language models

The notebook `Travel planner/agent.ipynb` shows how to wrap the retrieval logic in a tool and invoke it from an LLM. It uses the OpenAI function‑calling API to let the model decide when to call `trip_planner` and how to use the returned results. The agent then produces a formatted itinerary that includes flights, hotel and daily activities. This example highlights how LLMs can orchestrate data retrieval and reasoning via external tools.

### Weather‑aware agent

In `Travel planner/weather_agent.ipynb` the itinerary is further improved by consulting real‑time weather data. The notebook uses the geographical coordinates for each activity and queries a weather API for the forecast on the target dates. It then adjusts the plan—swapping indoor and outdoor activities, redistributing events across days and suggesting alternative locations—to ensure that travellers have the best possible experience.

## ChatGPT‑based storytelling

The `chatgpt_storytelling` folder contains a choose‑your‑own‑adventure narrative set in the fantasy realm of **Eldoria**. A party of heroes—**Aria** the ranger, **Finn** the mage and **Nyx** the rogue—explore enchanted forests, ancient ruins and treacherous dungeons. At key junctures the reader must choose between different paths, and each decision leads to a unique story branch. The interactive story is written entirely by ChatGPT without any additional code.

Important files include:
* `interactive_story.md` – The markdown version of the story with branching options.
* `interactive_story.docx` – A Word document for easy reading and printing.
* `images/eldoria.png` – An illustration of the Eldoria landscape.
* `README.md` – A short write‑up describing the characters and world.

To experience the story, open `interactive_story.md` and follow the numbered choices. Feel free to explore different branches to see how the heroes’ journey unfolds.

## Personal expense tracker

The `expense_tracker` directory contains a simple command‑line program (`personal_expense_tracker.py`) for managing personal finances. The tracker supports:

* Logging a new expense by entering the date, category, amount and an optional description.
* Viewing a list of all recorded expenses.
* Setting a monthly budget and tracking spending against it.
* Saving expenses to, and loading from, a CSV file so data persists across sessions.

The script uses Python’s standard library (`csv`, `datetime`) so there are no external dependencies. To run it, execute:

```bash
python personal_expense_tracker.py
```

You’ll be presented with a menu to add expenses, view expenses or set your budget. Data is stored in `expenses.csv` in the same folder.

## Getting started

Each project lives in its own sub‑directory. Clone the repository and navigate into the folder of interest to explore further:

```bash
git clone https://github.com/tinatsou/TinaAI.git
cd TinaAI/Travel\ planner    # or chatgpt_storytelling, expense_tracker
```

### Travel planner setup

The travel planner notebooks require Python 3.9+ and the following packages: `pandas`, `numpy`, `scikit‑learn`, `sentence‑transformers`, `openai`, `requests` and `matplotlib`. You can install them using:

```bash
pip install -r requirements.txt
```

Run the notebooks in Jupyter or VS Code and follow the instructions in each cell.

### Storytelling setup

The storytelling project doesn’t require any special setup—just open the markdown or Word file and read along. If you want to generate your own choose‑your‑own‑adventure stories, you can adapt the structure described in the README.

### Expense tracker setup

The expense tracker runs on Python’s standard library only. Run the script with Python 3.9+ and follow the on‑screen prompts to log expenses and manage your budget.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests. For bug reports or feature requests, please open an issue describing the problem and your proposed solution. Please make sure to follow the existing code style and include tests where appropriate.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

Thanks to the developers of the open‑source libraries used in these demos, including pandas, scikit‑learn, sentence‑transformers and OpenAI’s APIs. The choose‑your‑own‑adventure story was created using ChatGPT.
