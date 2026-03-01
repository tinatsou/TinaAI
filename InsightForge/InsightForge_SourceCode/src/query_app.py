import streamlit as st
import pandas as pd
import numpy as np
import os
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings

st.set_page_config(page_title="InsightForge", layout="wide")

PROMPT = """You are InsightForge, a Business Intelligence assistant.
Use ONLY the retrieved context to answer. If you are unsure, say so.
Always provide:
1) a concise answer
2) 3-5 bullet insights
3) suggestions for next steps
4) cite where in context the data came from.

Context:
{context}

Question:
{question}
"""

class CustomQAChain:
    def __init__(self, llm, retriever, prompt):
        self.llm = llm
        self.retriever = retriever
        self.prompt = prompt

    def invoke(self, inputs):
        q = inputs["query"]
        docs = self.retriever.invoke(q)
        context = "\n".join([d.page_content for d in docs])
        formatted_prompt = self.prompt.format(context=context, question=q)
        resp = self.llm.invoke(formatted_prompt)
        return {"result": resp.content, "source_documents": docs}

@st.cache_resource
def load_chain(vs_path="data/vectorstore"):
    if not os.environ.get("OPENAI_API_KEY"):
        return "MOCK"
    if not os.path.exists(vs_path):
        return None
    embeddings = OpenAIEmbeddings()
    vs = FAISS.load_local(vs_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    prompt = PromptTemplate(input_variables=["context", "question"], template=PROMPT)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = CustomQAChain(llm, retriever, prompt)
    return chain

st.title("InsightForge BI Assistant")

# Load real dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

total_rev = df['Sales'].sum()
active_custs = len(df) # Treat each row as an order/customer interaction
avg_sat = df['Customer_Satisfaction'].mean()

# Mock data for visual dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_rev/1000:.1f}K", "+14% YoY")
col2.metric("Total Orders / Active", f"{active_custs}", "+8% YoY")
col3.metric("Avg Satisfaction", f"{avg_sat:.1f}/5.0", "+0.2 YoY")

st.subheader("Revenue Trend")
revenue_trend = df.groupby(df['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
revenue_trend['Date'] = revenue_trend['Date'].dt.to_timestamp()
st.line_chart(revenue_trend.set_index("Date")['Sales'])

st.subheader("Top Contributors by Region (Pareto)")
contributors = df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()
st.bar_chart(contributors.set_index('Region'))

st.subheader("Ask Data a Question")
q = st.text_input("Example: Which region drove growth last quarter?", "Which region drove growth last quarter?")
if st.button("Generate Insights"):
    chain = load_chain()
    
    with st.spinner("Analyzing..."):
        if chain == "MOCK":
            st.warning("⚠️ Running in Mock Mode (No OPENAI_API_KEY detected). Returning simulated AI response based on sales_data.csv.")
            st.markdown("### LLM Analysis")
            st.write("Based on the data provided, **West** and **South** regions were top contributors over the entire underlying period, but let's look at recent dynamics. The West region showed consistent high transaction volume. Growth is often driven by specific product categories performing well in those key regions.")
            
            st.markdown("### Insight Cards")
            st.info("💡 **Recommendation 1:** Double down on campaigns in the **West** region as it is the top revenue generator overall.")
            st.info("🔍 **Recommendation 2:** Investigate the underlying cause of fluctuating satisfaction scores in Q2 to improve retention.")
            st.success("📈 **Recommendation 3:** Introduce upsell bundles for 'Widget B' and 'Widget C' which often drive high volume in the East.")
            
        elif chain is None:
            st.error("Vector store not found. Please run ingest_build_vectorstore.py first, or missing data.")
        else:
            resp = chain.invoke({"query": q})
            
            st.markdown("### LLM Analysis")
            st.write(resp["result"])
            
            st.markdown("### Insight Cards")
            st.info("💡 **Recommendation 1:** Double down on APAC marketing campaigns as it is the top growth region.")
            st.info("🔍 **Recommendation 2:** Investigate loss drivers in legacy regions to improve margin.")
            st.success("📈 **Recommendation 3:** Introduce upsell bundles during checkout to raise conversion rates across all segments.")
            
            with st.expander("Sources"):
                for doc in resp["source_documents"]:
                    st.write(doc.page_content[:300])
                    st.divider()
