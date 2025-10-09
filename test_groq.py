import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")  # optional if GROQ_API_KEY is set in env
)

# The invoke method expects a list of messages with roles, or a single string (as user message)
response = llm.invoke([{"role": "user", "content": "hi"}])

print(response.content)  # response is an AIMessage with a .content attribute
