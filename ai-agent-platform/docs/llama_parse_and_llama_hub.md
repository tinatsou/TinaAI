# LlamaParse and LlamaHub  

## Exploring LlamaParse  

LlamaParse is a GenAI‑powered document parser that extracts clean text from complex file formats.  A May 2025 update introduced support for newer models (GPT‑4.1 and Gemini 2.5 Pro), automatic orientation and skew detection, confidence scores for each parsed page, and more robust handling of page‑level errors ([www.llamaindex.ai](https://www.llamaindex.ai/blog/llamaparse-update-may-2025-new-models-skew-detection-and-more)).  These improvements mean your RAG pipeline starts with higher‑quality document chunks, and you can configure what happens when a page fails to parse (e.g., retry or skip).  

To experiment with LlamaParse, sign up for the free tier of **LlamaCloud** (it offers credits to process thousands of pages) and upload a PDF or Word document.  The API will return structured text with metadata like page numbers and confidence values.  You can also integrate LlamaParse into a script using the `llamactl` CLI.  

## Exploring LlamaHub  

LlamaHub is a community‑driven repository of connectors, agent tools and Llama Packs that plug into LlamaIndex ([llamahub.ai](https://llamahub.ai/#:~:text=Get%20your%20RAG%20application%20rolling,LlamaIndex%20%203%20%20LlamaIndex)).  It lets you quickly ingest data from sources like Notion, Slack, Google Drive, SQL databases and more without writing your own loaders.  Agent tools from LlamaHub can augment your agents with functions such as browsing, summarization or translation.  Llama Packs provide ready‑made project templates that combine connectors, indexes and query engines.  

Browse [llamahub.ai](https://llamahub.ai) to discover available loaders and tools.  Each entry includes installation instructions and usage examples.  By mixing and matching connectors and agents from LlamaHub, you can prototype new RAG applications in minutes.
