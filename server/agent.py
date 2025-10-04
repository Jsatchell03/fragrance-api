import os
import json
import pandas as pd

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

INDEX_PATH = "assets/faiss_index.bin"
EMB_MODEL = "all-MiniLM-L6-v2"

model = SentenceTransformer(EMB_MODEL)
index = faiss.read_index(INDEX_PATH)

df = pd.read_json("assets/perfume_data.json")


def get_recommendations(query, top_k=3):
    q_emb = model.encode([query], normalize_embeddings=True)
    D, I = index.search(q_emb.astype("float32"), top_k)
    results = df.iloc[I[0]][[
        'Perfume', 'Brand', 'Country', 'Gender', 'Rating Value',
        'Rating Count', 'Year', 'Top', 'Middle', 'Base', 'Perfumer1',
        'Perfumer2', 'mainaccord1', 'mainaccord2', 'mainaccord3',
        'mainaccord4', 'mainaccord5']]
    return results


@tool("perfume_recommender", return_direct=False)
def perfume_recommender(query: str) -> str:
    """
    Recommend perfumes similar to the user's scent description.
    Uses FAISS + precomputed SentenceTransformer embeddings.
    """
    results = get_recommendations(query)
    if not results:
        return "No close matches found."

    formatted = "\n".join(
        f"- {r['Perfume']} ({r['Brand']}, {r.get('Year', 'N/A')}) – similarity {r['similarity']:.3f}"
        for r in results
    )
    return f"Top matches based on your scent description:\n{formatted}"


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an AI fragrance assistant that helps users identify perfumes and colognes
            based on their descriptions. Use notes, accords, and scent families to provide
            helpful suggestions. If dataset tools are available, use them for more accurate answers.
            Always explain your reasoning in a friendly, clear way.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# For now, tools can be an empty list until teammate finishes the dataset
tools = [perfume_recommender]

# Create agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    query = input("What can I help you with today? ")
    response = agent_executor.invoke({"query": query})
    print(response["output"])
