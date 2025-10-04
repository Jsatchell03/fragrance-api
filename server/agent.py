import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

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
tools = []

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
