from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Trip Planner Backend", version="1.0")

# Allow frontend (Streamlit) calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 You can restrict later to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Graph/LLM once at startup
graph_builder = GraphBuilder(model_provider="groq")
react_app = graph_builder()

# Model for request validation
class QueryRequest(BaseModel):
    question: str

# ✅ Root route (prevents Render 404)
@app.get("/")
def root():
    return {"message": "✅ FastAPI Travel Planner Backend is running!"}

# 🚀 Main API endpoint
@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        # Optional: Generate and save graph
        try:
            png_graph = react_app.get_graph().draw_mermaid_png()
            with open("my_graph.png", "wb") as f:
                f.write(png_graph)
            print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        except Exception as e:
            print(f"⚠️ Graph rendering failed: {e}")

        # Pass user input to agent
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        # Parse AI output
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)
        
        return {"answer": final_output}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
